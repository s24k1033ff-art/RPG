using Godot;
using System;

/// <summary>
/// 【仕様書 2.1, 2.2, 5.2.②】を2D見下ろし平面RPG要素で大幅拡張
/// 8方向絶対移動、攻撃、VFS気流制御に加え、Eキーによる宝箱・扉・ショップとのインタラクト、およびゴールド・XPの獲得・吸い寄せを処理するメインコントローラー。
/// </summary>
public partial class PlayerController : CharacterBody2D, IVectorFlowInfluenced
{
    // --- アニメーション・ステート定義 ---
    public enum PlayerState
    {
        Idle,       // 待機
        Walk,       // 歩行
        Attack,     // 攻撃
        Dash,       // ダッシュ
        Hover       // 穴の上を滑空（ホバー）中
    }

    [ExportGroup("Dependencies")]
    /// <summary>
    /// プレイヤーステータス・アンロック状態のリソース。
    /// </summary>
    [Export] public PlayerData PlayerDataInstance { get; set; }

    [ExportGroup("Movement Stats")]
    [Export] public float MoveSpeed { get; set; } = 250.0f;
    [Export] public float DashSpeed { get; set; } = 650.0f;
    [Export] public float DashDuration { get; set; } = 0.15f;

    // --- 内部状態 ---
    private PlayerState _currentState = PlayerState.Idle;
    private VectorFlowHandler _vectorFlowHandler;
    
    // SP（スタミナ）とダッシュ関連変数
    private int _currentSP = 3; 
    private float _dashTimer = 0.0f;
    private float _spRecoveryTimer = 0.0f;
    private Vector2 _dashDirection = Vector2.Zero;

    // 攻撃関連変数
    private float _attackTimer = 0.0f;
    [Export] public float AttackDuration { get; set; } = 0.22f;

    // --- インターフェースプロパティ実装 ---
    public Vector2 CurrentFlowVector { get; set; } = Vector2.Zero;

    /// <summary>
    /// 現在通常の床（穴以外の安全な地面やトゲ床）にいるかどうかの判定。
    /// </summary>
    public bool IsOnNormalFloor { get; private set; } = true;

    public override void _Ready()
    {
        _vectorFlowHandler = GetNode<VectorFlowHandler>("VectorFlowHandler");
        
        if (PlayerDataInstance == null)
        {
            GD.Print("PlayerDataInstanceが設定されていないため、デフォルトで新規作成します。");
            PlayerDataInstance = new PlayerData();
        }

        if (_vectorFlowHandler != null)
        {
            _vectorFlowHandler.InitializePlayerData(PlayerDataInstance);
        }

        _currentSP = PlayerDataInstance.MaxHearts >= 3 ? PlayerDataInstance.Level + 2 : 3;
    }

    public override void _PhysicsProcess(double delta)
    {
        float fDelta = (float)delta;

        // 足元のタイル情報から穴判定
        UpdateFloorStatus();

        // ドロップオーブ（XPやゴールド）の吸い寄せと回収シミュレーション
        ProcessMagnetsAndCollect(fDelta);

        // タイマー更新と回復処理
        UpdateTimers(fDelta);

        // 各種状態遷移とアクション入力の検知
        HandleInput(fDelta);

        // 物理演算の適用
        MoveAndSlide();

        // 状態に基づきアニメーション・回転角を更新
        UpdateStateAndRotation();
    }

    private void UpdateFloorStatus()
    {
        // Godotプロジェクトに組み込む際は、エリア判定等で穴を検知します。
        IsOnNormalFloor = true; 

        if (!IsOnNormalFloor)
        {
            bool canHover = _currentState == PlayerState.Dash || 
                            _vectorFlowHandler.IsZeroFriction || 
                            (_vectorFlowHandler.FlowDirection != Vector2.Zero && 
                             Velocity.Dot(_vectorFlowHandler.FlowDirection) > 140f);

            if (canHover)
            {
                _currentState = PlayerState.Hover;
            }
            else
            {
                TriggerHazardDamage();
            }
        }
    }

    private void HandleInput(float delta)
    {
        if (_currentState == PlayerState.Dash || _currentState == PlayerState.Attack)
        {
            return;
        }

        // ベクトル流転の入力検知
        HandleVectorFlowShiftInput();

        // 8方向の入力ベクトルを取得
        Vector2 inputDir = Input.GetVector("move_left", "move_right", "move_up", "move_down");

        if (_vectorFlowHandler.IsZeroFriction)
        {
            Velocity += inputDir * MoveSpeed * 2.0f * delta;
            if (Velocity.Length() > MoveSpeed * 1.2f)
            {
                Velocity = Velocity.Normalized() * (MoveSpeed * 1.2f);
            }
        }
        else
        {
            if (inputDir != Vector2.Zero)
            {
                Velocity = inputDir * MoveSpeed;
            }
            else
            {
                Velocity = Velocity.Lerp(Vector2.Zero, 0.2f);
            }
        }

        // --- アクションのトリガー ---
        if (Input.IsActionJustPressed("attack"))
        {
            TriggerAttack();
        }

        if (Input.IsActionJustPressed("dash"))
        {
            TriggerDash();
        }

        if (Input.IsActionJustPressed("interact"))
        {
            TriggerInteract();
        }
    }

    private void HandleVectorFlowShiftInput()
    {
        if (!PlayerDataInstance.HasVectorFlowShift) return;

        if (Input.IsActionJustPressed("gvs_north")) // 北へ流す
        {
            _vectorFlowHandler.SetFlowDirection(Vector2.Up);
        }
        else if (Input.IsActionJustPressed("gvs_south")) // 南へ流す
        {
            _vectorFlowHandler.SetFlowDirection(Vector2.Down);
        }
        else if (Input.IsActionJustPressed("gvs_west")) // 西へ流す
        {
            _vectorFlowHandler.SetFlowDirection(Vector2.Left);
        }
        else if (Input.IsActionJustPressed("gvs_east")) // 東へ流す
        {
            _vectorFlowHandler.SetFlowDirection(Vector2.Right);
        }

        // 摩擦ゼロ（ホバー）モードの起動 (アンロックされている場合のみ可能)
        if (PlayerDataInstance.HasZeroFriction && Input.IsActionJustPressed("zero_g"))
        {
            _vectorFlowHandler.SetZeroFrictionState(!_vectorFlowHandler.IsZeroFriction);
        }
    }

    /// <summary>
    /// Eキーによるインタラクト（宝箱を開ける、鍵扉を開錠、ショップに触れる）の検出
    /// </summary>
    private void TriggerInteract()
    {
        GD.Print("[PlayerController] インタラクト開始：周囲のオブジェクト（宝箱、扉、ショップ碑石）を検出中...");
        
        // 周囲のコライダー（Area2DやRaycast）を検索し、対応する処理を実行します。
        // 実際のGodot上では、Area2Dなどで取得した対象が「どの鍵を必要とする扉か」を判定します。
        // 仮実装として "start" 鍵を要求する扉を想定します。
        string requiredKey = "start"; 

        if (PlayerDataInstance.HasKey(requiredKey))
        {
            PlayerDataInstance.UseKey(requiredKey);
            GD.Print($"[PlayerController] 🔑 【{requiredKey}の鍵】を使用し、封印の扉を開放しました！");
        }
        else
        {
            GD.Print($"[PlayerController] 宝箱を開く、またはショップ碑石を開くためのE入力を受け取りました。 (※扉を開けるには【{requiredKey}の鍵】が必要です)");
        }
    }

    /// <summary>
    /// ゴールドやXPドロップアイテムを吸い寄せ、回収する物理シミュレーション。
    /// </summary>
    private void ProcessMagnetsAndCollect(float delta)
    {
        // 実際の実装では、GetTree().GetNodesInGroup("Drops") 等を回し、
        // 距離110px以内であれば重力吸引（Lerpや加速度加算）を行い、
        // プレイヤーと接触（距離15px以下）したら回収してゴールドやXPを加算します。
    }

    /// <summary>
    /// 経験値を獲得し、レベルアップした場合は演出やパラメータ上昇を起動する。
    /// </summary>
    public void EarnXP(int amount)
    {
        bool leveledUp = PlayerDataInstance.GainXP(amount);
        if (leveledUp)
        {
            GD.Print($"✨ LEVEL UP! レベル {PlayerDataInstance.Level} に到達！ 最大HP・最大VPが上昇しました！");
            // 派手な光エフェクトや効果音を鳴らす処理をここに記述
        }
    }

    /// <summary>
    /// ゴールドを獲得する。
    /// </summary>
    public void EarnGold(int amount)
    {
        PlayerDataInstance.Gold += amount;
        GD.Print($"💰 +{amount} ゴールド獲得！ 合計: {PlayerDataInstance.Gold}G");
    }

    private void TriggerAttack()
    {
        if (_currentState == PlayerState.Dash) return;

        _currentState = PlayerState.Attack;
        _attackTimer = AttackDuration;

        GD.Print("[PlayerController] 次元剣スラッシュ！ ノックバックを気流にのせて敵を吹き飛ばす。");
        Velocity = Vector2.Zero;
    }

    private void TriggerDash()
    {
        if (_currentSP <= 0 || _currentState == PlayerState.Dash) return;

        _currentSP--;
        _spRecoveryTimer = 0.0f;

        _currentState = PlayerState.Dash;
        _dashTimer = DashDuration;

        Vector2 inputDir = Input.GetVector("move_left", "move_right", "move_up", "move_down");
        if (inputDir == Vector2.Zero)
        {
            inputDir = new Vector2(Mathf.Cos(Rotation), Mathf.Sin(Rotation));
        }

        _dashDirection = inputDir.Normalized();
        Velocity = _dashDirection * DashSpeed;
    }

    private void TriggerHazardDamage()
    {
        PlayerDataInstance.CurrentHearts -= 0.5f;
        
        GlobalPosition = new Vector2(80, 350); 
        Velocity = Vector2.Zero;
        _vectorFlowHandler.SetFlowDirection(Vector2.Zero);
        _vectorFlowHandler.SetZeroFrictionState(false);

        GD.Print($"[PlayerController] ハザード被弾！ 残りHP: {PlayerDataInstance.CurrentHearts}");
    }

    private void UpdateTimers(float delta)
    {
        if (_currentState == PlayerState.Attack)
        {
            _attackTimer -= delta;
            if (_attackTimer <= 0f)
            {
                _currentState = PlayerState.Idle;
            }
        }

        if (_currentState == PlayerState.Dash)
        {
            _dashTimer -= delta;
            if (_dashTimer <= 0f)
            {
                _currentState = PlayerState.Idle;
                Velocity = Vector2.Zero;
            }
        }

        // SP自動回復
        if (_currentSP < PlayerDataInstance.MaxHearts && _currentState != PlayerState.Dash)
        {
            _spRecoveryTimer += delta;
            if (_spRecoveryTimer >= 1.5f)
            {
                _currentSP = PlayerDataInstance.Level + 2; // レベルアップでSP最大値も少しスケール
                _currentSP = Mathf.Min(_currentSP, 5); // 最大5
                _spRecoveryTimer = 0.0f;
            }
        }
    }

    private void UpdateStateAndRotation()
    {
        if (_currentState != PlayerState.Attack && _currentState != PlayerState.Dash && _currentState != PlayerState.Hover)
        {
            if (Velocity.Length() > 10.0f)
            {
                _currentState = PlayerState.Walk;
                Rotation = Mathf.LerpAngle(Rotation, Mathf.Atan2(Velocity.Y, Velocity.X), 0.25f);
            }
            else
            {
                _currentState = PlayerState.Idle;
            }
        }
    }

    // --- インターフェースコールバック実装 ---

    public void OnVectorFlowChanged(Vector2 newDirection)
    {
        CurrentFlowVector = newDirection;
        GD.Print($"[PlayerController] 気流変更: {newDirection}");
    }

    public void SetZeroFriction(bool enabled)
    {
        if (enabled)
        {
            GD.Print("[PlayerController] ゼロ摩擦（ホバー）モード起動！ 慣性のみで滑ります。");
        }
        else
        {
            GD.Print("[PlayerController] ゼロ摩擦モード終了。床の通常摩擦が再適用されます。");
        }
    }

    // 互換用
    public void OnGravityDirectionChanged(Vector2 newDirection) {}
    public void SetZeroGravity(bool enabled) {}
}
