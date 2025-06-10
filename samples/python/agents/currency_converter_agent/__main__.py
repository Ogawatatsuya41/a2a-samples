# samples/python/agents/currency_converter_agent/main.py

import asyncio
import os
from typing import Annotated, Literal

from a2a.agents.google_adk import GoogleADKAgent, agent_prompt
from a2a.skills.skill_manager import SkillManager
from a2a.web.server import run_server
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# 簡単にするため、為替レートを固定
FIXED_EXCHANGE_RATES = {
    'EUR': {'USD': 1.07},
    'JPY': {'USD': 0.0064},
    'USD': {'EUR': 0.93, 'JPY': 157.0},
}

# スキル（エージェントの能力）を定義
class CurrencySkills(SkillManager):
    @staticmethod
    async def convert(
        amount: Annotated[float, '換算したい金額'],
        source_currency: Annotated[Literal['USD', 'EUR', 'JPY'], '換算元の通貨'],
        target_currency: Annotated[Literal['USD', 'EUR', 'JPY'], '換算先の通貨'],
    ) -> str:
        """指定された金額を、ある通貨から別の通貨に換算します。"""
        print(f"通貨換算スキルが呼ばれました: {amount} {source_currency} -> {target_currency}")
        if source_currency == target_currency:
            return f"{amount} {target_currency}"

        try:
            rate = FIXED_EXCHANGE_RATES[source_currency][target_currency]
            converted_amount = amount * rate
            result = f"{converted_amount:.2f} {target_currency}"
            print(f"換算結果: {result}")
            return result
        except KeyError:
            return "エラー: 対応していない通貨です。"

async def main():
    # エージェントの説明を定義
    agent = GoogleADKAgent(
        description='通貨換算を専門に行うエージェント。EUR, JPY, USD間の換算が可能です。',
        skills=CurrencySkills(),
        # このエージェントは自身で判断せず、依頼されたスキルを実行するだけ
        prompt_template=agent_prompt.skill_executor,
    )

    # サーバーをポート10003で起動
    # 環境変数 PORT があればそちらを優先
    port = int(os.getenv('PORT', '10003'))
    print(f'通貨換算エージェントを http://localhost:{port} で起動します')
    await run_server(agent, port=port)

if __name__ == '__main__':
    asyncio.run(main())