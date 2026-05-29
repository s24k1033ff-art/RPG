using Godot;

/// <summary>
/// 【仕様書 5.2.① 共通インターフェース・基盤コンポーネント】を2D見下ろし平面（XY軸）に最適化
/// 空間ベクトル流転（VFS）の影響を受けるすべての実体（Entity）が実装する共通インターフェース。
/// </summary>
public interface IVectorFlowInfluenced
{
    /// <summary>
    /// 現在のオブジェクトに適用されている空間のベクトル流（方向と強さ）。
    /// </summary>
    Vector2 CurrentFlowVector { get; set; }

    /// <summary>
    /// ベクトル流の方向が変更された時のコールバック。
    /// </summary>
    /// <param name="newDirection">新しいベクトル流の正規化された方向</param>
    void OnVectorFlowChanged(Vector2 newDirection);

    /// <summary>
    /// 摩擦ゼロ（ホバー）状態のオン/オフを設定する。
    /// </summary>
    /// <param name="enabled">摩擦ゼロを有効にするか</param>
    void SetZeroFriction(bool enabled);
}
