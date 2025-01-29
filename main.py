import asyncio
import twikit
from datetime import datetime
from zoneinfo import ZoneInfo
from httpx import AsyncClient
from bs4 import BeautifulSoup, ResultSet, Tag
from typing import Literal

client = twikit.Client(language="ja-JP")
client.load_cookies("cookies.json")

http = AsyncClient()


def checkContainMachLand(stores: ResultSet[Tag]) -> bool:
    for store in stores:
        print(store.text)
        if "テクノワールド" in store.text:
            return True
    return False


def checkMachLand(
    soup: BeautifulSoup,
) -> Literal["NEWSTORE", "REVIVAL", "RIP", "NOTMATCH"]:
    # 新規店舗
    newStore = soup.select_one('table[bgcolor="#F4C6C6"]')
    if not newStore:
        print("No New Store")
        return
    if checkContainMachLand(newStore.select('tr[style="color:#666666;"]')):
        return "NEWSTORE"

    # 復活店舗
    revivalStore = soup.select_one('table[bgcolor="#F4C6F4"]')
    if not revivalStore:
        print("No Revival Store")
        return
    if checkContainMachLand(revivalStore.select('tr[style="color:#666666;"]')):
        return "REVIVAL"

    # 消滅店舗
    ripStore = soup.select_one('table[bgcolor="#C6C6F4"]')
    if not ripStore:
        print("No RIP Store")
        return
    if checkContainMachLand(ripStore.select('tr[style="color:#666666;"]')):
        return "REVIVAL"

    return "NOTMATCH"


async def checkPLRS():
    # ポラリスコード ( POLARIS CHORD )
    response = await http.get("http://jtlppj.web.fc2.com/shop_ea/PLRS.html")
    response.encoding = "cp932"
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    flag = checkMachLand(soup)
    print(flag)

    match (flag):
        case "NEWSTORE":
            await client.create_tweet(
                "よくわかりませんが、新規店舗として #タイトーステーション盛岡マッハランド店 にて #ポラリスコード が稼働開始となりました。おめでとうございます。\n@Fng1Bot マッハランド行け"
            )
        case "REVIVAL":
            await client.create_tweet(
                "#タイトーステーション盛岡マッハランド店 にて #ポラリスコード が稼働開始となりました。おめでとうございます！！\n@Fng1Bot マッハランド行け"
            )
        case "RIP":
            await client.create_tweet(
                "#タイトーステーション盛岡マッハランド店 から #ポラリスコード が撤去されました。\n@Fng1Bot おつかれ"
            )
        case _:
            pass


async def checkNOS():
    # ノスタルジア ( Nostalgia )
    response = await http.get("http://jtlppj.web.fc2.com/shop_ea/NOSTALGIA.html")
    response.encoding = "cp932"
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    flag = checkMachLand(soup)
    print(flag)

    match (flag):
        case "NEWSTORE":
            await client.create_tweet(
                "よくわかりませんが、新規店舗として #タイトーステーション盛岡マッハランド店 にて #ノスタルジア が稼働開始となりました。おめでとうございます。\n@Fng1Bot"
            )
        case "REVIVAL":
            await client.create_tweet(
                "#タイトーステーション盛岡マッハランド店 にて #ノスタルジア が稼働開始となりました。おめでとうございます！！\n@Fng1Bot"
            )
        case "RIP":
            await client.create_tweet(
                "#タイトーステーション盛岡マッハランド店 から #ノスタルジア が撤去されました。\n@Fng1Bot"
            )
        case _:
            pass


async def checkPOPN():
    # ついでにポップン ( pop'n music )
    response = await http.get("http://jtlppj.web.fc2.com/shop_ea/PMSP.html")
    response.encoding = "cp932"
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    flag = checkMachLand(soup)
    print(flag)

    match (flag):
        case "NEWSTORE":
            await client.create_tweet(
                "よくわかりませんが、新規店舗として #タイトーステーション盛岡マッハランド店 にて #ポップン (pop'n music) が稼働開始となりました。おめでとうございます。\n@Fng1Bot"
            )
        case "REVIVAL":
            await client.create_tweet(
                "#タイトーステーション盛岡マッハランド店 にて #ポップン (pop'n music) が稼働開始となりました。おめでとうございます！！\n@Fng1Bot"
            )
        case "RIP":
            await client.create_tweet(
                "#タイトーステーション盛岡マッハランド店 から #ポップン (pop'n music) が撤去されました。\n@Fng1Bot"
            )
        case _:
            pass


async def main():
    while True:
        now = datetime.now(ZoneInfo("Asia/Tokyo"))
        # 8時に処理を開始
        if now.hour == 20 and now.minute == 33 and now.second == 0:
            await checkPLRS()
            await checkNOS()
            await checkPOPN()

        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
