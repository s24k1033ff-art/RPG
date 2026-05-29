using Godot;
using System;

/// <summary>
/// 【仕様書 5.3.② 壁抜け・埋まり防止のレイキャスト検知】を2D平面に最適化
/// ベクトル流に流されているときやホバー滑空から着地した際、キャラクターが壁の角にめり込んで動けなくなるバグを防ぐ
/// セーフティ・ポジショニング・コンポーネント。
/// </summary>
[GlobalClass]
public partial class SafetyPositioner : Node
{
    [ExportGroup("Collision Settings")]
    /// <summary>
    /// キャラクターのコリジョン半径（ピクセル単位）。
    /// </summary>
    [Export] public float CollisionRadius { get; set; } = 15.0f;

    /// <summary>
    /// 壁にめり込んでいると判定する安全マージン（ピクセル単位）。
    /// </summary>
    [Export] public float SafeMargin { get; set; } = 2.0f;

    // --- 内部参照 ---
    private CharacterBody2D _parentBody;
    private IVectorFlowInfluenced _flowInterface;

    public override void _Ready()
    {
        _parentBody = GetParent() as CharacterBody2D;
        _flowInterface = GetParent() as IVectorFlowInfluenced;

        if (_parentBody == null || _flowInterface == null)
        {
            GD.PrintErr("[SafetyPositioner] Error: 親ノードが CharacterBody2D かつ IVectorFlowInfluenced を実装していません。");
            SetPhysicsProcess(false);
        }
    }

    public override void _PhysicsProcess(double delta)
    {
        if (_parentBody == null) return;

        // 壁抜け防止めり込み強制補正の実行
        ResolveCollisionsAndPosition();
    }

    /// <summary>
    /// 【壁抜け・埋まり防止の位置補正アルゴリズム】
    /// 前後左右に物理レイキャストを飛ばし、めり込んでいる壁があれば即座に反対方向へ押し出す。
    /// </summary>
    private void ResolveCollisionsAndPosition()
    {
        var spaceState = _parentBody.GetWorld2D().DirectSpaceState;
        if (spaceState == null) return;

        Vector2 currentPosition = _parentBody.GlobalPosition;

        // 2D平面見下ろし型での4つの検査方向（上下左右）
        Vector2[] directions = new Vector2[] {
            Vector2.Up, Vector2.Down, Vector2.Left, Vector2.Right
        };

        foreach (Vector2 dir in directions)
        {
            Vector2 rayEnd = currentPosition + (dir * (CollisionRadius + SafeMargin));

            // 自分自身のコライダーを無視するレイキャストパラメータ
            var query = PhysicsRayQueryParameters2D.Create(currentPosition, rayEnd);
            query.Exclude = new Godot.Collections.Array<Rid> { _parentBody.GetRid() };

            // 衝突判定を実行
            var result = spaceState.IntersectRay(query);

            if (result.Count > 0)
            {
                Vector2 collisionPoint = (Vector2)result["position"];
                float distance = currentPosition.DistanceTo(collisionPoint);

                // コリジョン半径を下回っている（めり込んでいる）場合
                if (distance < CollisionRadius)
                {
                    float penetrationDepth = CollisionRadius - distance;

                    // 押し戻す方向
                    Vector2 resolveDir = (currentPosition - collisionPoint).Normalized();

                    // めり込んでいる距離分だけ、位置を安全にシフト
                    _parentBody.GlobalPosition += resolveDir * penetrationDepth;
                    
                    // めり込み方向の速度をゼロクリア
                    float velocityProjection = _parentBody.Velocity.Dot(resolveDir);
                    if (velocityProjection < 0)
                    {
                        _parentBody.Velocity -= resolveDir * velocityProjection;
                    }

                    currentPosition = _parentBody.GlobalPosition;

                    GD.Print($"[SafetyPositioner] VFS安全補正: 補正量={penetrationDepth:F2}px | 方向={resolveDir}");
                }
            }
        }
    }
}
