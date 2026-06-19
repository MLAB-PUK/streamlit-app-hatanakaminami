import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import os
from datetime import datetime
from streamlit_calendar import calendar

# ======================
# ページ設定
# ======================

st.set_page_config(
    page_title="ライブ記録",
    page_icon="🎤",
    layout="wide"
)

# ======================
# 曲リスト
# ======================

artist_songs = {

    "≒JOY": [
        "体育館ディスコ",
        "超孤独ライオン",
        "笑って フラジール",
        "今日も君の夢を見たんだ",
        "初恋シンデレラ",
        "ピーチティーとピーチパイ",
        "いま、月は満ちる",
        "The rock is you",
        "その先はイグザルト",
        "ノンフィクション",
        "ブルーハワイレモン",
        "「僕たちの歌」",
        "愛が痛かった",
        "アマガミガール",
        "今、恋をしている",
        "≒JOY",
        "ニアジョイ音頭",
        "電話番号教えて！",
        "夢見る♡アイドル",
        "0120お助け屋さん",
        "きっと、青い",
        "♡３か月♡",
        "大空、ビュンと",
        "無謀人",
        "だだだ、だって。",
        "スイートシックスティーン",
        "ネバギバ！生きろ",
        "overtune"
    ],

    "ずっと真夜中でいいのに。": [
        "アンチモン",
        "あいつら全員同窓会",
        "居眠り遠征隊",
        "ultra魂",
        "噓じゃない",
        "雲丹と栗",
        "上辺の私自身なんだよ",
        "奥底に眠るルーツ",
        "お勉強しといてよ",
        "形",
        "勘冴えて悔しいわ",
        "過眠",
        "海馬成長痛",
        "勘ぐれい",
        "蟹しゃぶふぁんく",
        "君がいて水になる",
        "綺羅キラー",
        "機械油",
        "繰り返す収穫",
        "グラスとラムレーズン",
        "暗く黒く",
        "クズリ念",
        "クリームで会いに行けますか",
        "蹴っ飛ばした毛布",
        "虚仮にしてくれ",
        "こんなこと騒動",
        "残機",
        "サターン",
        "彷徨い酔い温度",
        "シェードの埃は延長",
        "正義",
        "袖のキルト",
        "正しくなれない",
        "違う曲にしようよ",
        "地球存在しない説",
        "低血ボルト",
        "馴れ合いサーブ",
        "夏枯れ",
        "猫リセット",
        "脳裏上のクラッカー",
        "ばかじゃないのに",
        "はゔぁ",
        "ハゼ馳せる果てるまで",
        "花一匁",
        "微熱魔",
        "ヒューマノイド",
        "秒針を噛む",
        "不法侵入",
        "不死身の訓練",
        "またね幻",
        "間人間",
        "マイノリティ脈絡",
        "マリンブルーの庭園",
        "眩しいDNAだけ",
        "ミラーチューン",
        "胸の煙",
        "メディアノーチェ",
        "優しくLAST SMILE",
        "夜中のキスミ",
        "よもすがら",
        "ろんりねす",
        "Ham",
        "TAIDADA",
        "MILABO",
        "JK BOMBER",
        "Blues in the Closet",
        "Dear Mr 「F」",
        "lowmotion algae",
    ],

    "TREASURE": [
        "I WANT YOUR LOVE",
        "KING KONG",
        "SARURU",
        "MMM",
        "EVERYTHING",
        "NOW FOREVER",
        "BETTER THAN ME",
        "BONA BONA",
        "LAST NIGHT",
        "YELLOW",
        "I LOVE YOU",
        "JIKJIN",
        "HELLO",
        "B.L.T",
        "GOING CRAZY",
        "MY TREASURE",
        "RUN",
        "VolKno",
        "B.O.M.B",
        "ORANGE",
        "STUPID",
        "PARADISE",
        "BOY",
        "U",
        "COME TO ME",
        "CLAP!",
        "IT'S OKAY",
        "DARARI",
        "BEAUTIFUL",
        "SLOWMOTION",
        "BE WITH ME",
        "病",
        "THANK YOU",
        "HOLD IN",
        "MOVE",
        "Here I Stand",
        "LET IT BURN",
        "G.O.A.T",
        "THE WAY TO",
        "WONDERLAND",
        "WHATEVER,WHENEVER",
        "REVERSE",
        "BFF",
        "EVERYDAY"
    ],

    "EVERGLOW" :[
        "Bon Bon Chocolat",
        "Adios",
        "DUN DUN",
        "LA DI DA",
        "FIRST",
        "Pirate",
        "SLAY",
        "ZOMBI",
        "You Don't Know Me",
        "Moon",
        "Don't Speak",
        "Hush",
        "NO GOOD REASON",
        "DON'T ASK DON'T TELL",
        "PLEASE PLEASE",
        "UNTOUGHABLE",
        "GxxD BOY",
        "SALUTE",
        "PLAYER",
        "NO LIE",
        "D+1",
        "Back Together",
        "Nighty Night",
        "Company",
        "Oh Ma Ma Gad",
        "Make Me Feel",
        "Colourz",
        "BACK 2 LUV"

    ],

    "TOMORROW X TOGETHER":[
        "Dejavu",
        "Over The Moon",
        "0X1=LOVESONG (I Know I Love You)",
        "Devil by the Window",
        "Sugar Rush Ride",
        "Farewell, Neverland",
        "Resist(Not Gonna Run Away)",
        "New Rules",
        "LO$ER=LO♡ER",
        "Higher Than Heaven",
        "Thursday’s Child Has Far To Go Rise",
        "君じゃない誰かの愛し方 (Ring)",
        "Quarter Life",
        "The Killa (I Belong to You)",
        "Tinnitus (돌멩이가 되고 싶어)",
        "Danger",
        "Back for More (TXT Ver.)",
        "GGUM",
        "Good Boy Gone Bad",
        "Growing Pain",
        "Dreamer",
        "Forty One Winks",
        "I’ll See You There Tomorrow",
        "Magic Island",
        "Heaven",
        "Happily Ever After",
        "きっとずっと(Kitto Zutto)",
        "MOA Diary",
        "９と４分の３番線で君を待つ (Run Away)",
        "Chasing That Feeling",
        "Magic",
        "Forse",
        "ひとりの夜",
        "Trust Fund Baby",
        "PUMA",
        "ひとつの誓い",
        "Miracle",
        "紫陽花のような恋",
    ]


}

# ======================
# uploadsフォルダ
# ======================

if not os.path.exists("uploads"):
    os.makedirs("uploads")

# ======================
# DB接続
# ======================

conn = sqlite3.connect(
    "live_records.db",
    check_same_thread=False
)

c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS lives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    artist TEXT,
    venue TEXT,
    seat TEXT,
    setlist TEXT,
    memo TEXT,
    image_path TEXT
)
""")

conn.commit()

# ======================
# タイトル
# ======================

st.title("🎤 ライブ記録")

tab1, tab2 = st.tabs([
    "➕ ライブ登録",
    "📅 カレンダー"
])

# ======================
# ライブ登録
# ======================

with tab1:

    st.header("➕ ライブ登録")

    date = st.date_input("📅 ライブ日")

    artist = st.selectbox(
        "🎤 アーティスト",
        list(artist_songs.keys())
    )

    venue = st.text_input("🏟 会場")

    seat = st.text_input("🪑 席")

    # アーティストごとの曲表示
    selected_songs = st.multiselect(
        "🎵 セトリ",
        options=artist_songs[artist]
    )

    # 番号付きセトリ
    setlist = "\n".join(
        [
            f"{i+1}. {song}"
            for i, song in enumerate(selected_songs)
        ]
    )

    st.text_area(
        "確認用セトリ",
        value=setlist,
        height=200
    )

    memo = st.text_area("💭 感想")

    uploaded_file = st.file_uploader(
        "📸 写真",
        type=["png", "jpg", "jpeg"]
    )

    # 保存ボタン
    if st.button("💾 保存"):

        image_path = ""

        if uploaded_file is not None:

            timestamp = datetime.now().strftime(
                "%Y%m%d%H%M%S"
            )

            image_path = (
                f"uploads/"
                f"{timestamp}_{uploaded_file.name}"
            )

            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        c.execute("""
        INSERT INTO lives (
            date,
            artist,
            venue,
            seat,
            setlist,
            memo,
            image_path
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(date),
            artist,
            venue,
            seat,
            setlist,
            memo,
            image_path
        ))

        conn.commit()

        st.success("ライブ記録を保存しました！")
        


    st.divider()

    # ======================
    # ライブ一覧
    # ======================

    st.header("📖 ライブ一覧")

    df = pd.read_sql_query(
        "SELECT * FROM lives ORDER BY date DESC",
        conn
    )

    if len(df) == 0:

        st.info("まだライブ記録がありません")

    else:

        for index, row in df.iterrows():

            with st.expander(
                f"{row['date']} - {row['artist']}"
            ):

                new_artist = st.selectbox(
                    "🎤 アーティスト",
                    list(artist_songs.keys()),
                    index=list(
                        artist_songs.keys()
                    ).index(row["artist"]),
                    key=f"artist_{row['id']}"
                )

                new_venue = st.text_input(
                    "🏟 会場",
                    row["venue"],
                    key=f"venue_{row['id']}"
                )

                new_seat = st.text_input(
                    "🪑 席",
                    row["seat"],
                    key=f"seat_{row['id']}"
                )

                # 曲リスト
                song_options = artist_songs[new_artist]

                # 現在のセトリを取得
                current_setlist = []

                if row["setlist"]:

                    lines = row["setlist"].split("\n")

                    for line in lines:

                        if ". " in line:

                            current_setlist.append(
                                line.split(". ", 1)[1]
                            )

                
                # 存在する曲だけ残す
                valid_default_songs = [
                   song for song in current_setlist
                    if  song in song_options
                ]

# 編集用セトリ
                new_selected_songs = st.multiselect(
                    "🎵 セトリ",
                    options=song_options,
                    default=valid_default_songs,
                    key=f"edit_setlist_{row['id']}"
                )
                # 番号付きに変換
                new_setlist = "\n".join(
                    [
                        f"{i+1}. {song}"
                        for i, song in enumerate(
                            new_selected_songs
                        )
                    ]
                )

                new_memo = st.text_area(
                    "💭 感想",
                    row["memo"],
                    key=f"memo_{row['id']}"
                )

                # 画像表示
                if row["image_path"] != "":

                    if os.path.exists(
                        row["image_path"]
                    ):

                        image = Image.open(
                            row["image_path"]
                        )

                        st.image(image, width=300)

                col1, col2 = st.columns(2)

                # 更新
                with col1:

                    if st.button(
                        "✏️ 更新",
                        key=f"update_{row['id']}"
                    ):

                        c.execute("""
                        UPDATE lives
                        SET
                            artist=?,
                            venue=?,
                            seat=?,
                            setlist=?,
                            memo=?
                        WHERE id=?
                        """, (
                            new_artist,
                            new_venue,
                            new_seat,
                            new_setlist,
                            new_memo,
                            row["id"]
                        ))

                        conn.commit()

                        st.success("更新しました！")

                        st.rerun()

                # 削除
                with col2:

                    if st.button(
                        "🗑 削除",
                        key=f"delete_{row['id']}"
                    ):

                        # 画像削除
                        if row["image_path"] != "":

                            if os.path.exists(
                                row["image_path"]
                            ):

                                os.remove(
                                    row["image_path"]
                                )

                        c.execute(
                            "DELETE FROM lives WHERE id=?",
                            (row["id"],)
                        )

                        conn.commit()

                        st.warning("削除しました")

                        st.rerun()

# ======================
# カレンダー
# ======================

# ======================
# カレンダー
# ======================

# ======================
# カレンダー
# ======================

with tab2:

    st.header("📅 ライブカレンダー")

    # DB取得
    df = pd.read_sql_query(
        "SELECT * FROM lives",
        conn
    )

    # イベント作成
    events = []

    for _, row in df.iterrows():

        events.append({
            "title": row["artist"],
            "start": row["date"],
            "id": str(row["id"])
        })

    # カレンダー設定
    calendar_options = {
        "initialView": "dayGridMonth",
        "locale": "ja",
        "height": 700,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth"
        }
    }

    # カレンダー表示
    calendar_result = calendar(
        events=events,
        options=calendar_options,
        key="live_calendar"
    )

    # ======================
    # ライブ詳細
    # ======================

    if calendar_result:

        # イベントクリック時
        if "eventClick" in calendar_result:

            clicked_event = (
                calendar_result["eventClick"]["event"]
            )

            live_id = clicked_event["id"]

            c.execute(
                "SELECT * FROM lives WHERE id=?",
                (live_id,)
            )

            live = c.fetchone()

            if live:

                st.divider()

                st.subheader("🎤 ライブ詳細")

                st.write(f"📅 日付: {live[1]}")
                st.write(f"🎤 アーティスト: {live[2]}")
                st.write(f"🏟 会場: {live[3]}")
                st.write(f"🪑 席: {live[4]}")

                st.subheader("🎵 セトリ")
                st.text(live[5])

                st.subheader("💭 感想")
                st.write(live[6])

                # 画像
                if live[7] != "":

                    if os.path.exists(live[7]):

                        image = Image.open(live[7])

                        st.image(image, width=400)