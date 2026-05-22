import flet as ft
import csv
import random
import io

def get_all_words():
    # 請在此貼上你完整 2127 個單字的 CSV 內容
    raw_csv_data = """單字 (Word),詞性 (POS),中文翻譯
abandon,v.,放棄
ability,n.,能力
aboard,adv./prep.,在船(飛機/車)上
about,prep./adv.,關於
above,prep./adv.,在...上方"""
   accord        	[n]一致、符合
    acceptable    	[a]可接受的, 合意的
    accident      	[n]意外事件, 事故
    account        	[n]計算, 帳目, 說明, 估計, 理由；[vi]說明, 總計有, 認為, 得分；[vt]認為
    accurate      	[a]正確的, 精確的
    ache          	[n]疼痛；[vi]覺得疼痛, 渴望
    achieve        	[vt]完成, 達到
    achievement    	[n]成就, 功勣
    activity      	[n]活躍, 活動性, 行動, 行為, 放射性
  actual        	[a]實際的, 真實的, 現行的, 目前的
  ad            	[n]廣告； Andorra , 安道爾；[縮] Air Defense, 防空
  additional    	[a]另外的, 附加的, 額外的
  admire        	[v]讚美, 欽佩, 羨慕
  admit          	[v]容許, 承認, 接納
  adopt          	[vt]採用, 收養
  advanced      	[a]高級的, 年老的, 先進的
  advantage      	[n]優勢, 有利條件, 利益
  adventure      	[n]冒險, 冒險的經歷；[v]冒險
  advertisement  	[n]廣告, 做廣告
  advice        	[n]忠告, 建議, 通知
  adviser / advisor	[n]顧問, <美>(學生的)指導老師
  affect        	[vt]影響, 感動, 侵襲, 假裝
  afford        	[vt]提供, 給予, 供應得起
  afterwards    	[副]然後, 後來地
  agriculture    	[n]農業, 農藝, 農學
  air-conditioner	[n]空調機
  alley          	[n]小路, 巷, (花園裡兩邊有樹籬的)小徑
  amaze          	[vt]使吃驚
  amazement      	[n]驚愕, 驚異
  ambassador    	[n]大使
  ambition      	[n]野心, 雄心
  angel          	[n]天使, 完善可愛的人
  angle          	[n]角, 角落；[vi]釣魚, 追逐
  announce      	[vt]宣佈, 通告
  announcement  	[n]宣告, 發表, 一項公告, 一項私人告示
  apart          	[副]分離, 分成零件, 分別地, 分離著；[a]分開的
  apparent      	[a]顯然的, 外觀上的
  appeal        	[n]請求, 呼籲, 上訴, 吸引力, 要求；[vi]求助, 訴請, 要求；[vt]控訴
  appreciate    	[vt]賞識, 鑒賞, 感激；[vi]增值, 漲價
  approach      	[n]接近, 逼近, 走進, 方法, 步驟, 途徑, 通路；[vt]接近, 動手處理；[vi]靠近
  approve        	[vi]贊成, 滿意；[vt]批准, 通過；[v]批准
  aquarium      	[n]養魚池, 玻璃缸, 水族館
  arrival        	[n]到來, 到達, 到達者
  ash            	[n]灰, 灰燼, 岑樹
  aside          	[副]在旁邊, 到旁邊
  assist        	[v]援助, 幫助
  athlete        	[n]運動員, 運動選手
  attempt        	[n]努力, 嘗試, 企圖；[vt]嘗試, 企圖
  attitude      	[n]姿勢, 態度, 看法, 意見
  attract        	[vt]吸引；[vi]有吸引力, 引起注意
  attractive    	[a]吸引人的, 有魅力的
  audience      	[n]聽眾, 觀眾, 接見, 拜見
  author        	[n]作家, 創造者
  auto          	[n]<美口>汽車
  automatic      	[n]自動機械；[a]自動的, 無意識的, 機械的
  automobile    	[n]<主美>汽車(=<英> motor car,car)
  available      	[a]可用到的, 可利用的, 有用的, 有空的, 接受探訪的
  avenue        	[n]林蔭道, 大街, 方法, 途徑, 路
  average        	[n]平均, 平均水平, 平均數, 海損；[a]一般的, 通常的, 平均的；[vt]平均為, 均分, 使平衡；[vi]買進, 賣出
  awake          	[vi]醒, 覺醒, 領會, 覺悟；[vt]喚醒；[a]警覺的, 醒的
  awaken        	[v]喚醒, 醒來, 喚起
  award          	[n]獎, 獎品；[vt]授予, 判給
  aware          	[a]知道的, 明白的, 意識到的
  awful          	[a]可怕的, 威嚴的, <口>極度的, 糟糕的
  ax            	[n]斧頭；[vt]削減
  axe            	[n]斧, (經費的)大削減
  background    	[n]背景, 後台, 不重要或不引人注目的地方或位置
  bacon          	[n]鹹肉, 燻肉
  bacteria      	[n]細菌
  badly          	[副]嚴重地, 惡劣地
  badminton      	[n]羽毛球
  baggage        	[n]行李, 輜重
  bait          	[n]餌, 誘惑物；
  balance        	[n]天平, 平衡, 收支差額, 結余, 余額；[v]平衡,
  bandage        	[n]繃帶
  bare          	[a]赤裸的, 無遮蔽的, 空的；[vt]使赤裸, 露出
  barely        	[副]僅僅, 剛剛, 幾乎不能
  barn          	[n]穀倉, 畜棚, 畜舍, 機器房
  barrel        	[n]桶；[vt]裝入桶內
  bay            	[n]海灣, 狗吠聲, 絕路；[vt]吠, 使走投無路；[vi]吠
  beam          	[n]梁, 桁條, (光線的)束, 柱, 電波, 橫梁；[v]播送
  beast          	[n]獸, 畜牲, 人面獸心的人
  beggar        	[n]乞丐
  behave        	[vi]舉動, 舉止, 運轉；[v]行為表現
  belly          	[n]腹部, 胃；[vi]漲滿
  beneath        	[副]在...之下；[介]在...之下
  benefit        	[n]利益, 好處；[vt]有益于, 有助于；[vi]受益
  berry          	[n]漿果
  Bible          	[n]《聖經》
  billion        	[n][a]十億(的)
  bingo          	[n]一種賭博游戲, 烈酒
  biscuit        	[n]餅乾, 小點心
  blanket        	[n]毯子；[vt]覆蓋
  bleed          	[v]使出血, 放血
  bless          	[vt]祝福, 保祐
  bold          	[a]大膽的；[n]粗體
  boot          	[n]<美>(長統)靴, 靴子
  border        	[n]邊界, 國界, 邊, 邊沿, 邊境
  bore          	[v]使煩擾
brake          	[n]閘, 剎車；[v]剎車
bravery        	[n]勇敢
breast        	[n]胸部, 乳房, 胸懷, 心情；[vt]以胸對著, 對付
breath        	[n]呼吸, 氣息, 氣味, 空氣, 微風, 暫停, 瞬間
breathe        	[v]呼吸, 發出
breeze        	[n]微風
bride          	[n]新娘
brilliant      	[a]燦爛的, 閃耀的, 有才氣的
brook          	[n]小溪；[vt]容忍
broom          	[n]掃帚, 金雀花；[vt]掃除
brow          	[n]眉毛, 額, (面部)表情
bubble        	[n]泡沫, 幻想的計劃；[vi]起泡, 潺潺的流
bucket        	[n]桶, 一桶的量, 鏟斗
bud            	[n]芽, 蓓蕾；[vi]發芽, 萌芽
budget        	[n]預算；[vi]做預算, 編入預算
buffalo        	[n](印度,非洲等的)水牛；<美>美洲野牛
buffet        	[n]餐具櫃, 小賣部, 毆打, 打擊；[v]打擊, 搏斗
bulb          	[n]鱗莖, 球形物
bull          	[n]公牛, 粗壯如牛的人
bullet        	[n]子彈
bunch          	[n]串, 束v.捆成一束
burden        	[n]擔子, 負擔；[v]負擔
burglar        	[n]夜賊
bury          	[vt]埋葬, 掩埋, 隱藏
bush          	[n]矮樹叢, (機械)襯套
buzz          	[n]嗡嗡聲；[v]作嗡嗡聲, 嗡嗡作響, 逼近

    
    f = io.StringIO(raw_csv_data.strip())
    return list(csv.DictReader(f))

def main(page: ft.Page):
    page.title = "早餐單字機 3.0"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.padding = 20

    all_words = get_all_words()
    session_words = []
    current_index = 0
    
    # 核心安全修正：改用符合新版 Flet 規範的方法呼叫，確保跨天記憶
    def get_storage(key):
        try:
            return page.get_client_storage().get(key) or []
        except:
            return []

    def set_storage(key, value):
        try:
            page.get_client_storage().set(key, value)
        except:
            pass

    word_display = ft.Text("皇翔單字機", size=45, weight="bold", color="blue")
    pos_display = ft.Text("", size=18, italic=True, color="grey")
    mean_display = ft.Text("請選擇模式開始", size=24, color="black")
    stat_text = ft.Text("", size=16, color="grey")
    total_info = ft.Text("", size=14)

    def update_total_info():
        rem = get_storage("rem_list")
        forg = get_storage("forg_list")
        total_info.value = f"累計標記 -> O: {len(rem)} | X: {len(forg)}"
        page.update()

    def update_ui():
        if session_words:
            w = session_words[current_index]
            word_val = w.get('單字 (Word)') or list(w.values())[0]
            pos_val = w.get('詞性 (POS)') or list(w.values())[1]
            mean_val = w.get('中文翻譯') or list(w.values())[2]
            
            word_display.value = word_val
            pos_display.value = f"({pos_val})" if pos_val else ""
            mean_display.value = mean_val
            stat_text.value = f"目前進度: {current_index + 1} / {len(session_words)}"
            page.update()

    def mark(status):
        nonlocal current_index
        if not session_words or word_display.value in ["練習結束", "無資料"]: return
        
        # 建立唯一 ID
        w_id = f"{word_display.value}_{mean_display.value}"
        rem = get_storage("rem_list")
        forg = get_storage("forg_list")
        
        if status == "O":
            if w_id not in rem: rem.append(w_id)
            if w_id in forg: forg.remove(w_id)
        else:
            if w_id not in forg: forg.append(w_id)
            if w_id in rem: rem.remove(w_id)
            
        set_storage("rem_list", rem)
        set_storage("forg_list", forg)
        update_total_info()

        if current_index < len(session_words) - 1:
            current_index += 1
            update_ui()
        else:
            word_display.value = "練習結束"
            pos_display.value = ""
            mean_display.value = "切換模式繼續複習"
            page.update()

    def start_session(mode):
        nonlocal session_words, current_index
        if not all_words: return
        
        rem = get_storage("rem_list")
        forg = get_storage("forg_list")

        if mode == "30":
            session_words = random.sample(all_words, min(30, len(all_words)))
        elif mode == "review_o":
            session_words = [w for w in all_words if f"{(w.get('單字 (Word)') or list(w.values())[0])}_{(w.get('中文翻譯') or list(w.values())[2])}" in rem]
        elif mode == "review_x":
            session_words = [w for w in all_words if f"{(w.get('單字 (Word)') or list(w.values())[0])}_{(w.get('中文翻譯') or list(w.values())[2])}" in forg]
        
        if not session_words:
            word_display.value = "無資料"
            pos_display.value = ""
            mean_display.value = "清單目前是空的"
            page.update()
        else:
            current_index = 0
            update_ui()

    def reset_all():
        try:
            page.get_client_storage().clear()
        except:
            pass
        update_total_info()
        word_display.value = "已重置"
        pos_display.value = ""
        mean_display.value = "紀錄已清除"
        page.update()

    # 極簡無干擾 UI
    page.add(
        ft.Column([
            ft.Text("皇翔單字機 3.0", size=18, weight="bold"),
            total_info,
            ft.Divider(),
            word_display,
            pos_display,
            mean_display,
            stat_text,
            ft.Container(height=10),
            ft.Row([
                ft.ElevatedButton("O 記得", on_click=lambda _: mark("O"), bgcolor="green", color="white"),
                ft.ElevatedButton("X 忘記", on_click=lambda _: mark("X"), bgcolor="red", color="white"),
            ], alignment="center"),
            ft.Divider(),
            ft.Row([
                ft.OutlinedButton("隨機 30 題", on_click=lambda _: start_session("30")),
                ft.OutlinedButton("複習 X", on_click=lambda _: start_session("review_x")),
                ft.OutlinedButton("複習 O", on_click=lambda _: start_session("review_o")),
            ], alignment="center"),
            ft.TextButton("清除所有紀錄", on_click=lambda _: reset_all())
        ], horizontal_alignment="center")
    )
    update_total_info()

ft.app(target=main)
