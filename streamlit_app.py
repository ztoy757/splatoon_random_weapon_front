import html
import json
import os
import random
from typing import Any, Dict, List, Optional

import requests
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="Splatoon3 Random Weapon Generator",
    page_icon="🦑",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# カスタムCSS
st.markdown(
    """
<style>
    .weapon-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }
    
    .weapon-name {
        font-size: 1.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .weapon-category {
        font-size: 1.1em;
        color: #ffeb3b;
        margin-bottom: 8px;
    }
    
    .weapon-detail {
        font-size: 0.9em;
        opacity: 0.9;
        margin: 3px 0;
    }
    
    .main-title {
        text-align: center;
        color: #2c3e50;
        font-size: 3em;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .generate-button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 1.2em;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
</style>
""",
    unsafe_allow_html=True,
)


class WeaponService:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv("MOCKOON_API_URL", "http://mockoon:3000")

    def get_random_weapon(self) -> Optional[Dict[str, Any]]:
        """Mockoon APIのrandom-weaponエンドポイントから1つの武器を取得"""
        try:
            response = requests.get(f"{self.base_url}/random-weapon", timeout=5)
            response.raise_for_status()
            weapon_data = response.json()
            return weapon_data
        except requests.exceptions.Timeout:
            st.error("API接続がタイムアウトしました")
            return None
        except requests.exceptions.ConnectionError:
            st.error("APIサーバーに接続できませんでした")
            return None
        except requests.exceptions.HTTPError as e:
            st.error(f"HTTP エラー: {e.response.status_code}")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"API接続エラー: {str(e)}")
            return None
        except (json.JSONDecodeError, ValueError) as e:
            st.error(f"レスポンス解析エラー: {str(e)}")
            return None

    def get_random_weapons(self, count: int = 8) -> List[Dict[str, Any]]:
        """random-weaponエンドポイントを複数回呼び出して指定数の武器を取得"""
        weapons = []
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i in range(count):
            status_text.text(f"武器を取得中... ({i+1}/{count})")
            weapon = self.get_random_weapon()

            if weapon:
                weapons.append(weapon)
                st.success(f"✅ 武器 {i+1}: {weapon.get('name', '不明')} を取得しました")
            else:
                st.warning(f"⚠️ 武器 {i+1} の取得に失敗しました")
                # フォールバック武器データ
                fallback_weapon = {
                    "id": i + 1,
                    "name": f"フォールバック武器 {i+1}",
                    "category": "シューター",
                    "sub_weapon": "スプラッシュボム",
                    "special_weapon": "ウルトラショット",
                }
                weapons.append(fallback_weapon)

            progress_bar.progress((i + 1) / count)

        progress_bar.empty()
        status_text.empty()

        if weapons:
            st.success(f"🎉 {len(weapons)}個の武器データを取得完了!")

        return weapons


def display_weapon_card(weapon: Dict[str, Any]) -> None:
    """武器カードを表示"""
    category_colors = {
        "シューター": "#ff6b6b",
        "チャージャー": "#4ecdc4",
        "ローラー": "#45b7d1",
        "フデ": "#96ceb4",
        "スピナー": "#feca57",
        "マニューバー": "#ff9ff3",
        "スロッシャー": "#54a0ff",
        "シェルター": "#5f27cd",
        "ストリンガー": "#00d2d3",
        "ワイパー": "#ff6348",
    }

    color = category_colors.get(weapon["category"], "#667eea")

    # HTMLサニタイゼーション
    safe_name = html.escape(str(weapon.get("name", "不明")))
    safe_category = html.escape(str(weapon.get("category", "不明")))
    safe_sub_weapon = html.escape(str(weapon.get("sub_weapon", "不明")))
    safe_special_weapon = html.escape(str(weapon.get("special_weapon", "不明")))

    st.markdown(
        f"""
    <div class="weapon-card" style="background: linear-gradient(135deg, {color} 0%, #764ba2 100%);">
        <div class="weapon-name">{safe_name}</div>
        <div class="weapon-category">{safe_category}</div>
        <div class="weapon-detail">サブ: {safe_sub_weapon}</div>
        <div class="weapon-detail">スペシャル: {safe_special_weapon}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def main():
    """メイン画面"""

    # タイトル
    st.markdown(
        '<h1 class="main-title">🦑 Splatoon3 Random Weapon Generator 🐙</h1>',
        unsafe_allow_html=True,
    )

    # サービス初期化
    weapon_service = WeaponService()

    # セッション状態の初期化
    if 'selected_weapons' not in st.session_state:
        st.session_state.selected_weapons = []

    # ボタンとオプション
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        weapon_count = st.slider("選択する武器数", min_value=1, max_value=18, value=8, step=1)

        if st.button("🎲 ランダム武器を生成", type="primary", use_container_width=True):
            with st.spinner("武器を選択中..."):
                st.session_state.selected_weapons = weapon_service.get_random_weapons(
                    weapon_count
                )

    # 選択された武器を表示
    if st.session_state.selected_weapons:
        st.markdown("---")
        st.markdown("### 🎯 選択された武器")

        # 4列のグリッドレイアウト
        cols_per_row = 4
        weapons = st.session_state.selected_weapons

        for i in range(0, len(weapons), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, weapon in enumerate(weapons[i : i + cols_per_row]):
                with cols[j]:
                    display_weapon_card(weapon)

        # 統計情報
        st.markdown("---")
        st.markdown("### 📊 選択武器の統計")

        col1, col2 = st.columns(2)

        with col1:
            category_count = {}
            for weapon in weapons:
                category = weapon["category"]
                category_count[category] = category_count.get(category, 0) + 1

            st.markdown("**カテゴリー別分布:**")
            for category, count in sorted(category_count.items()):
                st.write(f"- {category}: {count}個")

        with col2:
            sub_weapons = [weapon["sub_weapon"] for weapon in weapons]
            special_weapons = [weapon["special_weapon"] for weapon in weapons]

            st.markdown("**サブウェポン:**")
            for sub in set(sub_weapons):
                count = sub_weapons.count(sub)
                if count > 1:
                    st.write(f"- {sub} (×{count})")
                else:
                    st.write(f"- {sub}")


if __name__ == "__main__":
    main()
