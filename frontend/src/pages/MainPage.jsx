import {useState, useEffect} from 'react';
import axios from 'axios';
import { CartesianGrid, Line, LineChart, Tooltip, XAxis, YAxis, Legend, matchByDataKey, Label, BarChart, Bar, ResponsiveContainer, DefaultZIndexes} from 'recharts';
import './mainpage.css';

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="custom-tooltip">
        <p className="label">{`${label} : ${payload[0].value}`}</p>
        <div>
          {payload.map((pld) => (
            <p style={{ display: "flex", padding: 10 }}>
              <div style={{ color: pld.fill }}>{pld.value}</div>
              <div> {pld.dataKey}</div>
            </p>
          ))}
        </div>
      </div>
    );
  }

  return null;
};

export default function MainPage() {

    const [metrics, setMetrics] = useState([]);
    const [currentMetrics, setCurrentMetrics] = useState([]);

    const formatPercent = (value) => `${value}%`;
    const formatDiskSpace = (value) => `${(value / (1024 * 1024 * 1024)).toFixed(0)}GB`;



    const loadData = () => {
        axios.get('http://localhost:8000/api/metrics/?last=15').then(response => {
            setMetrics(response.data);
            // console.log('Fetched metrics:', response.data);
        }).catch(error => {
            console.error('Error fetching metrics:', error);
        });
    }

    useEffect(() => {
        loadData();
        let interval = setInterval(() => loadData(), (1000 * 30)); // fetch data every 30 seconds

        const socket = new WebSocket("ws://localhost:8000/ws/dashboard/");

        socket.onmessage = (event) => {
            const data = JSON.parse(String(event.data));
            setCurrentMetrics([
                { name: "CPU", value: data.cpu_usage },
                { name: "RAM", value: data.ram_usage },
                { name: "Dysk", value: data.disk_used },
            ]);
        };

        socket.onopen = () => {
            console.log("Connected");
        };
        
        socket.onerror = (err) => {
            console.error(err);
        };

        socket.onclose = () => {
            console.log("Disconnected");
        };


        return () => {
            socket.close();
            clearInterval(interval)
        }
    }
    ,[]);
        

  return (
    <div className="main-page">
        <div className='content'>
            <div className='metric-title'>Server Metrics:</div>
            <div className='current-metrics'>
                {currentMetrics[0] !== undefined && <div className='metric'>CPU: {formatPercent(currentMetrics[0].value)}</div>}
                {currentMetrics[1] !== undefined && <div className='metric'>RAM: {formatPercent(currentMetrics[1].value)}</div>}
                {currentMetrics[2] !== undefined && <div className='metric'>Disk: {formatDiskSpace(currentMetrics[2].value)}</div>}
            </div>
            <div className='charts'>
                <LineChart className='metric-chart'  style={{ width: '100%', aspectRatio: 1.618, maxWidth: 600 }} responsive data={metrics}>
                    <CartesianGrid strokeDasharray="2 2"/>
                    <Label  style={{ textAnchor: 'middle' }} value="CPU Usage" position="insideTop"/>
                    {/* <Tooltip contentStyle={{backgroundColor: '#901a1a'}} wrapperStyle={{zIndex: 1000, backgroundColor: '#901a1a'}} className='chart-tooltip' allowEscapeViewBox={{"x":true,"y":true}} animationDuration={0} formatter={formatPercent}/> */}
                    <Tooltip allowEscapeViewBox={{"x":true,"y":true}} wrapperStyle={{zIndex: 1000, backgroundColor: '#901a1a'}} animationDuration={0} formatter={formatPercent} content={<CustomTooltip />} cursor={{ fill: "transparent" }} />
                    {/* <CustomTooltip/> */}
                    <Legend verticalAlign="top" align="right" />
                    <Line isAnimationActive={false} type="monotone" dot={{}} dataKey="cpu_usage_max" stroke="#d88484" />
                    <Line isAnimationActive={false} type="monotone" dot={{}} dataKey="cpu_usage_avg" stroke="#d8d184"/>
                    <Line isAnimationActive={false} type="monotone" dot={{}} dataKey="cpu_usage_min" stroke="#84d8d5" />

                    <XAxis dataKey="timestamp" />
                    <YAxis type="number" domain={[0, 100]} />

                </LineChart>
                <LineChart className='metric-chart' style={{ width: '100%', aspectRatio: 1.618, maxWidth: 600 }} responsive data={metrics}>
                    <CartesianGrid />
                    <Label style={{ textAnchor: 'middle' }} value="RAM Usage" position="insideTop" />
                    <Line isAnimationActive={false} type="monotone" dataKey="ram_usage_max" stroke="#d88484" />
                    <Line isAnimationActive={false} type="monotone" dataKey="ram_usage_avg"  stroke="#d8d184"/>
                    <Line isAnimationActive={false} type="monotone" dataKey="ram_usage_min"  stroke="#84d8d5" />

                    <XAxis dataKey="timestamp" />
                    <YAxis type="number" domain={[0, 100]} />
                </LineChart>
                <LineChart className='metric-chart' style={{ width: '100%', aspectRatio: 1.618, maxWidth: 600 }} responsive data={metrics}>
                    <CartesianGrid />
                    <Label style={{ textAnchor: 'middle' }} value="Disk Space" position="insideTop" />
                    <Tooltip allowEscapeViewBox={{"x":true,"y":true}} animationDuration={0} formatter={formatDiskSpace}/>
                    <Line isAnimationActive={false} dataKey="disk_used" stroke="#84d8d5" formatter={formatDiskSpace} />
                    <XAxis dataKey="timestamp" />
                    <YAxis type="number" domain={[0, 1099511627776]} tickFormatter={formatDiskSpace} />
                </LineChart>
            </div>
        </div>
    </div>
  );
}