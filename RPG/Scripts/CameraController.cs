using Godot;
using System;

/// <summary>
/// 【仕様書 5.3.① 画面向きの完全固定カメラ】に準拠
/// マップの向きは常に 0度 に固定（3D酔いを完全に防止）し、プレイヤーを滑らかに追従する2Dカメラリグ。
/// </summary>
[GlobalClass]
public partial class CameraController : Camera2D
{
    [ExportGroup("Target")]
    /// <summary>
    /// 追従対象のプレイヤーコントローラー。
    /// </summary>
    [Export] public PlayerController TargetPlayer { get; set; }

    [ExportGroup("Smooth Settings")]
    /// <summary>
    /// カメラの位置追従のスムーズさ（Lerpの重み）。
    /// </summary>
    [Export] public float PositionSmoothSpeed { get; set; } = 10.0f;

    public override void _Ready()
    {
        // 追従対象が設定されていない場合、自動的にアクティブなプレイヤーを検索
        if (TargetPlayer == null)
        {
            TargetPlayer = GetTree().GetFirstNodeInGroup("Player") as PlayerController;
        }

        if (TargetPlayer == null)
        {
            GD.PrintErr("[CameraController] Warning: TargetPlayer が設定されていません。プレイヤーを 'Player' グループに追加するか、インスペクターからアタッチしてください。");
        }
    }

    public override void _PhysicsProcess(double delta)
    {
        if (TargetPlayer == null) return;

        float fDelta = (float)delta;

        // 1. 位置の追従（通常のカメラ追従）
        GlobalPosition = GlobalPosition.Lerp(TargetPlayer.GlobalPosition, PositionSmoothSpeed * fDelta);

        // 2. 【3D酔い対策・UI最適化】
        // マップの向きは常に固定（Rotation = 0）に維持し、パズルアクションの認知負荷を最小限に抑えます。
        Rotation = 0.0f;
    }
}
