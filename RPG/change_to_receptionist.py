import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 描画テキストの変更 (📜 [E] クエストボード -> 👩‍💼 [E] 受付嬢 (クエスト))
html = html.replace("📜 [E] クエストボード", "👩‍💼 [E] ギルド受付嬢")

# 2. UIパネルのHTML変更
# <h2 style="color: #4facfe; margin-bottom: 20px;">📜 ギルド クエストボード</h2> 
# などを書き換える
html = html.replace("📜 ギルド クエストボード", "👩‍💼 ギルド受付嬢")

# 3. JavaScript ロジックの変更 (セリフ調にする)
old_new_quest = "\"<h3 style='color:#4ade80'>新規クエストを受注しました！</h3><br>目的: \" + player.activeQuest.name + \"<br>報酬: \" + player.activeQuest.reward + \"G\""
new_new_quest = "\"<p>いらっしゃいませ、冒険者様。</p><h3 style='color:#4ade80'>現在のおすすめクエストはこちらです！</h3><br>目的: \" + player.activeQuest.name + \"<br>報酬: \" + player.activeQuest.reward + \"G<br><br><p style='font-size:14px; color:#aaa'>※依頼を達成したらまた私に話しかけてくださいね。</p>\""
html = html.replace(old_new_quest, new_new_quest)

old_report = "\"<h3 style='color:#fcd34d'>クエスト報告完了！</h3><br>報酬 \" + player.activeQuest.reward + \"G を獲得しました！\""
new_report = "\"<p>お帰りなさいませ！依頼の達成、確認いたしました。</p><h3 style='color:#fcd34d'>クエスト完了です！お疲れ様でした。</h3><br>報酬として \" + player.activeQuest.reward + \"G をお渡しします。\""
html = html.replace(old_report, new_report)

old_progress = "\"<h3 style='color:#fff'>現在進行中のクエスト</h3><br>目的: \" + player.activeQuest.name + \"<br>進行度: \" + player.questProgress + \" / \" + player.activeQuest.req"
new_progress = "\"<p>いつもお疲れ様です。</p><h3 style='color:#fff'>現在進行中のクエスト状況です</h3><br>目的: \" + player.activeQuest.name + \"<br>進行度: \" + player.questProgress + \" / \" + player.activeQuest.req + \"<br><br><p style='font-size:14px; color:#aaa'>無理せず頑張ってくださいね！</p>\""
html = html.replace(old_progress, new_progress)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Quest board updated to Receptionist successfully.')
