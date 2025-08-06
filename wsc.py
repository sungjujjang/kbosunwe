import asyncio
import websockets
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import pandas as pd
from html_table_parser import parser as parser
import undetected_chromedriver as uc
import json

EXTRA_RANK = { # w d l
    "Samsung Lions" : [0, 0, 0],
    "LG Twins" : [0, 0, 0],
    "Lotte Giants" : [0, 0, 0],
    "KIA Tigers" : [0, 0, 0],
    "KT Wiz" : [0, 0, 0],
    "Kiwoom Heroes" : [0, 0, 0],
    "SSG Landers" : [0, 0, 0],
    "Doosan Bears" : [0, 0, 0],
    "Hanwha Eagles" : [0, 0, 0],
    "NC Dinos" : [0, 0, 0],
}

TEAMS = {
    "Kia" : "KIA Tigers",
    "Kiwoom" : "Kiwoom Heroes",
    "Lotte" : "Lotte Giants",
    "LG" : "LG Twins",
    "NC" : "NC Dinos",
    "Samsung" : "Samsung Lions",
    "SSG" : "SSG Landers",
    "Doosan" : "Doosan Bears",
    "Hanwha" : "Hanwha Eagles",
    "KT" : "KT Wiz"
}

def search_team_rank_in_won_rank(team_name, list):
    for team in list:
        if team['team'] == team_name:
            return team['rank']
    return None
    

class KboDataset:
    def __init__(self):
        options = Options()
        self.driver = uc.Chrome(options=options)
        self.driver.get("https://mykbostats.com/")
        
    def get_kbo_rankings(self):
        self.driver.refresh()
        self.driver.implicitly_wait(1)
        html = str(self.driver.page_source)
        soup = BeautifulSoup(html, "html.parser")

        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.select('tbody.syncscroll tr')
        
        rankings = []
        temp_rank = []
        
        won_rank = []
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 7:
                continue
            
            rank = int(cols[0].text.strip().split()[0])
            team_name = cols[0].find('a').text.strip()
            wins = int(cols[1].text.strip())
            losses = int(cols[2].text.strip())
            draws = int(cols[3].text.strip())
            win_rate = float(cols[4].text.strip())
            game_gap = float(cols[5].text.strip())
            # recent = cols[6].text.strip()
            
            won_rank.append({
                "rank": rank,
                "team": team_name,
            })

            if team_name in EXTRA_RANK:
                wins += EXTRA_RANK[team_name][0]
                losses += EXTRA_RANK[team_name][2]
                draws += EXTRA_RANK[team_name][1]
            
            win_rate = round(wins / (wins + losses), 3)
                
            temp_rank.append([team_name, wins, losses, draws, win_rate])
        
        one_sung = 0
        
        for rank, (team_name, wins, losses, draws, win_rate) in enumerate(sorted(temp_rank, key=lambda x: (-x[4])), start=1):
            if rank == 1:
                one_sung = wins - losses
                game_gap = 0
            else:
                game_gap = round((one_sung - (wins - losses))/2, 1)

            rankings.append({
                "rank": rank,
                "team": team_name,
                "win": wins,
                "lose": losses,
                "draw": draws,
                "winRate": win_rate,
                "gap": game_gap
            })
        
        updown = []
        for i in range(len(won_rank)):
            rk = rankings[i]['rank']
            wr = search_team_rank_in_won_rank(rankings[i]['team'], won_rank)
            print(f"{rankings[i]['team']} 순위: {rk}, 원랭크: {wr}")
            if rk == wr:
                print(f"{rankings[i]['team']} 순위 변동 없음")
                continue
            elif rk < wr:
                updown.append({
                    'rank': f"{abs(wr - rk)} ▲",
                    'direction': "up",
                    'team': rankings[i]['team']
                })
            else:
                updown.append(
                    {
                        'rank': f"{abs(wr - rk)} ▼",
                        'direction': "down",
                        'team': rankings[i]['team']
                    }
                )
            
        return rankings, updown
    

    def parse_game_score(self):
        html = str(self.driver.page_source)
        soup = BeautifulSoup(html, 'html.parser')
        games = []

        global EXTRA_RANK
        init_extra_rank()
        for game in soup.select('#home__games__today a.game-line'):
            try:
                team1 = game.select_one('.away-team').contents[0].strip()
                team2 = game.select_one('.home-team').contents[0].strip()
                
                t1c = game.select_one('.away-score')
                t2c = game.select_one('.home-score')
                
                if not t1c or not t2c:
                    continue
                
                score1 = int(t1c.text.strip())
                score2 = int(t2c.text.strip())
                
                is_finished = "false"
                
                if game.select_one('.inning'):
                    if game.select_one('.inning').text.strip() == "Final":
                        is_finished = "true"
                        
                team1 = TEAMS.get(team1, team1)
                team2 = TEAMS.get(team2, team2)
                
                if score1 > score2:
                    EXTRA_RANK[team1][0] = 1
                    EXTRA_RANK[team2][2] = 1
                    # print(f"{team1} 승리")
                elif score1 < score2:
                    EXTRA_RANK[team2][0] = 1
                    EXTRA_RANK[team1][2] = 1
                    # print(f"{team2} 승리")
                else:
                    EXTRA_RANK[team1][1] = 1
                    EXTRA_RANK[team2][1] = 1
                    # print(f"{team1} {team2} 무승부")


                games.append({
                    'team1': team1,
                    'team2': team2,
                    'team1_score': score1,
                    'team2_score': score2,
                    'is_finished': is_finished
                })
            except Exception as e:
                print(f"파싱 실패: {e}")
                continue

        return games

def init_extra_rank():
    global EXTRA_RANK
    EXTRA_RANK = { # w d l
        "Samsung Lions" : [0, 0, 0],
        "LG Twins" : [0, 0, 0],
        "Lotte Giants" : [0, 0, 0],
        "KIA Tigers" : [0, 0, 0],
        "KT Wiz" : [0, 0, 0],
        "Kiwoom Heroes" : [0, 0, 0],
        "SSG Landers" : [0, 0, 0],
        "Doosan Bears" : [0, 0, 0],
        "Hanwha Eagles" : [0, 0, 0],
        "NC Dinos" : [0, 0, 0],
    }

RANKTEXT = None
SCORETEXT = None
UPDOWN = None
        
connected_clients = set()

async def gkb():
    kbo_dataset = KboDataset()
    global RANKTEXT
    global SCORETEXT
    global UPDOWN
    while True:
        t = kbo_dataset.get_kbo_rankings()
        RANKTEXT = str(t[0])
        SCORETEXT = str(kbo_dataset.parse_game_score())
        UPDOWN = str(t[1])
        await asyncio.sleep(10)  # 10초 간격으로 갱신

async def handler(websocket):
    connected_clients.add(websocket)
    print(f"{len(connected_clients)}명 접속 중")
    await websocket.send("순위" + str(RANKTEXT).replace("'", '"'))
    await websocket.send("스코어" + str(SCORETEXT).replace("'", '"'))
    await websocket.send("업다운" + str(UPDOWN).replace("'", '"'))

    try:
        async for message in websocket:
            print(f"클라이언트로부터 메시지 수신: {message}")
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)
        print(f"클라이언트 종료됨. 남은 연결 수: {len(connected_clients)}")

async def broadcast(message):
    if connected_clients:
        await asyncio.gather(*[client.send(message) for client in connected_clients])

async def periodic_broadcast():
    count = 1
    while True:
        if not RANKTEXT:
            await asyncio.sleep(5)
        await broadcast("순위" + str(RANKTEXT).replace("'", '"'))
        await broadcast("스코어" + str(SCORETEXT).replace("'", '"'))
        await broadcast("업다운" + str(UPDOWN).replace("'", '"'))
        print(f">> {count}회차")
        print(f">>> {UPDOWN}")
        print(f">>> {SCORETEXT}")
        print(f">>> {RANKTEXT}")
        count += 1
        await asyncio.sleep(5)  # 5초 간격

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("웹소켓 서버 실행 중 (localhost:8765)")
        await asyncio.gather(
            asyncio.Future(),
            periodic_broadcast(),
            gkb()
        )

if __name__ == "__main__":
    asyncio.run(main())
