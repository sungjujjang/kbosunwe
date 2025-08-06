import './App.css';
import { sum } from 'es-toolkit';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, Table } from 'react-bootstrap';

import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

import { useState, useEffect, useRef } from 'react';
import { set } from 'es-toolkit/compat';


function App() {

  const [rankList, setRankList] = useState([]);
  const [liveScore, setLiveScore] = useState([]);
  const [updown, setUpdown] = useState([]);

  const ws = useRef(null);
  const uri = 'ws://localhost:8765'
  var Loading = true;

  useEffect(() => {
    ws.current = new WebSocket(uri);
    ws.current.onopen = () => {
      console.log('open')
      Loading = false;
    }
    ws.current.onmessage = (event) => {
      if (event.data) {
        if (event.data.startsWith('순위')) {
          const data = JSON.parse(event.data.substr(2));
          if (data.length > 0) {
            setRankList(data);
          }
        } else if (event.data.startsWith('스코어')) {
          const data = JSON.parse(event.data.substr(3));
          if (data.length > 0) {
            setLiveScore(data);
          } 
        } else if (event.data.startsWith('업다운')) {
            const data = JSON.parse(event.data.substr(3));
            console.log(data);
            if (data.length > 0) {
              setUpdown(data);
            }
          }
      }
    };
    ws.current.onerror = () => console.log('Error');
    ws.current.onclose = () => {
      alert('웹소켓 연결이 끊어졌습니다. 재연결을 시도합니다.');
      ws.current = new WebSocket(uri);
    };

    return () => {
      if (ws.current && ws.current.readyState === 1) {
        ws.current.close();
      }
    };
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <Navbar expand="lg" className="bg-body-tertiary">
          <Container>
            <Navbar.Brand href="#home">KBO LIVE RANK</Navbar.Brand>
          </Container>
        </Navbar>
        <div className="parent">
          <div className="div1">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th scope="col">순위</th>
                  <th scope="col">팀</th>
                  <th scope="col">승</th>
                  <th scope="col">무</th>
                  <th scope="col">패</th>
                  <th scope="col">승률</th>
                  <th scope="col">게임차</th>
                </tr>
              </thead>
              <tbody>
                {rankList.map((item) => (
                  <tr key={item.rank}>
                    <td>{item.rank}</td>
                    <td>{item.team}</td>
                    <td>{item.win}</td>
                    <td>{item.draw}</td>
                    <td>{item.lose}</td>
                    <td>{item.winRate.toFixed(3)}</td>
                    <td>{item.gap}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="div2">
            <table className="table table-striped">
                {updown.length === 0 ? (
                  <>
                    <thead>
                        <tr>
                          <th scope="col">순위변동</th>
                        </tr>
                    </thead>
                    <tbody><td>순위 변동이 없습니다.</td></tbody>
                  </>
                ) : (
                  <>
                    <thead>
                        <tr>
                          <th scope="col">팀</th>
                          <th scope="col">순위변동</th>
                        </tr>
                    </thead>
                    <tbody>
                      {updown.map((item, idx) => (
                        <tr key={idx}>
                          <td>{item.team}</td>
                          <td>{item.rank}</td>
                        </tr>
                      ))}
                    </tbody>
                  </>
                )}
              </table>
          </div>
          <div className="div3">
            <table className="table table-striped">
              
              {liveScore.length === 0 ? (
                <>
                  <thead>
                      <tr>
                        <th scope="col">경기</th>
                      </tr>
                  </thead>
                  <tbody><td>현재 진행 중인 경기가 없습니다</td></tbody>
                </>
              ) : (
                <>
                  <thead>
                      <tr>
                        <th scope="col">팀</th>
                        <th scope="col">스코어</th>
                        <th scope="col">팀</th>
                      </tr>
                  </thead>
                  <tbody>
                    {liveScore.map((item, idx) => (
                      <tr key={idx}>
                        <td>{item.team1}</td>
                        <td>{item.team1_score} : {item.team2_score}</td>
                        <td>{item.team2}</td>
                      </tr>
                    ))}
                  </tbody>
                </>
              )}
            </table>
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
