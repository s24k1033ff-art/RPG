using Godot;
using System;
using System.Collections.Generic;

/// <summary>
/// 【仕様書 2.3.2, 5.2】
/// プレイヤーの各種ステータス、レベル、XP、アンロック状態、および特定エリア用の鍵リストを保持するデータコンテナ。
/// </summary>
public partial class PlayerData : Resource
{
    [Export] public int Level { get; set; } = 1;
    [Export] public int XP { get; set; } = 0;
    [Export] public int XPNeeded { get; set; } = 50;
    [Export] public int Gold { get; set; } = 0;
    
    // --- 新システム：エリア固有の鍵リスト ---
    /// <summary>
    /// 獲得済みの鍵のIDリスト（例: "start", "forest", "crystal", "temple"）。
    /// これにより、シーケンスブレイク（別のエリアの鍵で違う扉を開ける）を防止します。
    /// </summary>
    [Export] public Godot.Collections.Array<string> UnlockedKeys { get; set; } = new Godot.Collections.Array<string>();

    [Export] public float MaxHearts { get; set; } = 3.0f;
    [Export] public float CurrentHearts { get; set; } = 3.0f;

    [Export] public float MaxVP { get; set; } = 100.0f;
    [Export] public float CurrentVP { get; set; } = 100.0f;

    // アンロック能力
    [Export] public bool HasVectorFlowShift { get; set; } = true;
    [Export] public bool HasZeroFriction { get; set; } = false;

    public PlayerData() {}

    /// <summary>
    /// 経験値を獲得し、レベルアップの閾値を超えた場合はステータスを上昇させます。
    /// </summary>
    /// <param name="amount">獲得するXP量</param>
    /// <returns>レベルアップした場合はtrue</returns>
    public bool GainXP(int amount)
    {
        XP += amount;
        if (XP >= XPNeeded)
        {
            XP -= XPNeeded;
            Level++;
            XPNeeded = Mathf.FloorToInt(XPNeeded * 1.5f);
            
            MaxHearts = Mathf.Min(6.0f, MaxHearts + 0.5f);
            CurrentHearts = MaxHearts;
            
            MaxVP += 20.0f;
            CurrentVP = MaxVP;
            
            return true;
        }
        return false;
    }

    /// <summary>
    /// 特定の鍵を持っているか確認します。
    /// </summary>
    public bool HasKey(string keyId)
    {
        return UnlockedKeys.Contains(keyId);
    }

    /// <summary>
    /// 鍵を消費（使用）します。
    /// </summary>
    public void UseKey(string keyId)
    {
        if (UnlockedKeys.Contains(keyId))
        {
            UnlockedKeys.Remove(keyId);
        }
    }

    /// <summary>
    /// 鍵を獲得します。
    /// </summary>
    public void AddKey(string keyId)
    {
        if (!UnlockedKeys.Contains(keyId))
        {
            UnlockedKeys.Add(keyId);
        }
    }
}
