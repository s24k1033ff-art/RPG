using Godot;
using System;

/// <summary>
/// 【仕様書 5.2.① 共通インターフェース・基盤コンポーネント】を2D見下ろし平面に最適化
/// 空間ベクトル流転（VFS）の影響を受けるキャラクターにアタッチし、空間気流物理とエネルギー（VP）を管理するコンポーネント。
/// </summary>
[GlobalClass]
public partial class VectorFlowHandler : Node
{
    /// <summary>
    /// 現在の空間気流（ベクトル流）の方向を表す正規化ベクトル。
    /// Vector2.Zero は大気が静穏（流れなし）な状態。
    /// </summary>
    public Vector2 FlowDirection { get; private set; } = Vector2.Zero;

    /// <summary>
    /// ベクトル流の推進加速力。
    /// </summary>
    [Export] public float FlowStrength { get; set; } = 320.0f;

    /// <summary>
    /// 摩擦ゼロ（ホバー）状態フラグ。
    /// </summary>
    public bool IsZeroFriction { get; private set; } = false;

    // --- 内部参照 ---
    private CharacterBody2D _parentBody;
    private IVectorFlowInfluenced _flowInterface;
    private PlayerData _playerData; // プレイヤーの場合のみ、VPの同期に使用

    public override void _Ready()
    {
        _parentBody = GetParent() as CharacterBody2D;
        _flowInterface = GetParent() as IVectorFlowInfluenced;

        if (_parentBody == null || _flowInterface == null)
        {
            GD.PrintErr($"[VectorFlowHandler] Error: 親ノードが CharacterBody2D かつ IVectorFlowInfluenced を実装していません。ノード名: {GetParent()?.Name}");
            SetPhysicsProcess(false);
        }
    }

    /// <summary>
    /// プレイヤー用のPlayerDataをセットし、VPの同期を有効にする。
    /// </summary>
    public void InitializePlayerData(PlayerData data)
    {
        _playerData = data;
    }

    public override void _PhysicsProcess(double delta)
    {
        if (_parentBody == null) return;

        float fDelta = (float)delta;

        // 接地状態の取得（親がPlayerControllerの場合はそのIsOnFloor等と連携）
        // 2D見下ろし型においては、穴の上にいないことを「通常接地（OnFloor）」と定義します。
        bool isOnFloor = true;
        if (_parentBody is PlayerController playerCtrl)
        {
            isOnFloor = playerCtrl.IsOnNormalFloor;
        }

        // 【仕様書 2.3.② VPリソース管理の2D最適化】
        HandleVP(isOnFloor, fDelta);

        // 【空間気流物理の適用】
        // ベクトル流が発生している場合、恒常的な流れの力をVelocityに加算します。
        if (FlowDirection != Vector2.Zero)
        {
            _parentBody.Velocity += FlowDirection * FlowStrength * fDelta;
        }
    }

    /// <summary>
    /// ベクトル流の方向を動的に変更する。
    /// </summary>
    /// <param name="newDirection">新しいベクトル流の方向ベクトル</param>
    public void SetFlowDirection(Vector2 newDirection)
    {
        if (newDirection == Vector2.Zero)
        {
            FlowDirection = Vector2.Zero;
        }
        else
        {
            FlowDirection = newDirection.Normalized();
        }
        _flowInterface.OnVectorFlowChanged(FlowDirection);
    }

    /// <summary>
    /// 摩擦ゼロ（ホバー）ステートを切り替える。
    /// </summary>
    public void SetZeroFrictionState(bool enabled)
    {
        IsZeroFriction = enabled;
        _flowInterface.SetZeroFriction(enabled);
    }

    /// <summary>
    /// VP（ベクトルエネルギー）リソース管理。
    /// </summary>
    private void HandleVP(bool isOnFloor, float delta)
    {
        if (_playerData == null) return;

        bool isVFSActive = FlowDirection != Vector2.Zero || IsZeroFriction || !isOnFloor;

        if (isOnFloor && !isVFSActive)
        {
            // 接地しており、流れもホバーも無効ならVP急速回復
            _playerData.CurrentVP = Mathf.MoveToward(
                _playerData.CurrentVP,
                _playerData.MaxVP,
                _playerData.VpRecoveryRate * delta
            );
        }
        else if (isVFSActive)
        {
            // ベクトル流転中、ホバー中、または穴の上の滑空中はエネルギー消費
            _playerData.CurrentVP = Mathf.MoveToward(
                _playerData.CurrentVP,
                0f,
                _playerData.VpConsumptionRate * delta
            );

            // VPが枯渇したら強制リセット
            if (_playerData.CurrentVP <= 0f)
            {
                ResetFlowToNormal();
            }
        }
    }

    /// <summary>
    /// VP枯渇時に静穏・通常摩擦状態に戻す。
    /// </summary>
    private void ResetFlowToNormal()
    {
        if (IsZeroFriction)
        {
            SetZeroFrictionState(false);
        }
        if (FlowDirection != Vector2.Zero)
        {
            SetFlowDirection(Vector2.Zero);
        }
    }
}
