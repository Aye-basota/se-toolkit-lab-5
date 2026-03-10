import React, { useEffect, useState } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';

// Регистрация компонентов Chart.js
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

// Строгие TypeScript интерфейсы (никаких 'any')
interface ScoreBucket {
    bucket: string;
    count: number;
}

interface TimelineEntry {
    date: string;
    submissions: number;
}

interface PassRate {
    task: string;
    avg_score: number;
    attempts: number;
}

export default function Dashboard() {
    const [lab, setLab] = useState<string>('lab-04');
    const [scores, setScores] = useState<ScoreBucket[]>([]);
    const [timeline, setTimeline] = useState<TimelineEntry[]>([]);
    const [passRates, setPassRates] = useState<PassRate[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            setError(null);
            try {
                const token = localStorage.getItem('api_key');
                const headers = {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                };

                const API_URL = import.meta.env.VITE_API_TARGET || '';

                const [scoresRes, timelineRes, passRatesRes] = await Promise.all([
                    fetch(`${API_URL}/analytics/scores?lab=${lab}`, { headers }),
                    fetch(`${API_URL}/analytics/timeline?lab=${lab}`, { headers }),
                    fetch(`${API_URL}/analytics/pass-rates?lab=${lab}`, { headers })
                ]);

                if (!scoresRes.ok || !timelineRes.ok || !passRatesRes.ok) {
                    throw new Error('Failed to fetch analytics data');
                }

                const scoresData: ScoreBucket[] = await scoresRes.json();
                const timelineData: TimelineEntry[] = await timelineRes.json();
                const passRatesData: PassRate[] = await passRatesRes.json();

                setScores(scoresData);
                setTimeline(timelineData);
                setPassRates(passRatesData);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Unknown error');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [lab]);

    const barData = {
        labels: scores.map(s => s.bucket),
        datasets: [
            {
                label: 'Scores Distribution',
                data: scores.map(s => s.count),
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
            },
        ],
    };

    const lineData = {
        labels: timeline.map(t => t.date),
        datasets: [
            {
                label: 'Submissions per day',
                data: timeline.map(t => t.submissions),
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.2,
            },
        ],
    };

    return (
        <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
            <h2>Analytics Dashboard</h2>

            <div style={{ marginBottom: '20px' }}>
                <label htmlFor="lab-select" style={{ marginRight: '10px', fontWeight: 'bold' }}>Select Lab: </label>
                <select
                    id="lab-select"
                    value={lab}
                    onChange={(e) => setLab(e.target.value)}
                    style={{ padding: '8px', borderRadius: '4px' }}
                >
                    <option value="lab-01">Lab 01</option>
                    <option value="lab-02">Lab 02</option>
                    <option value="lab-03">Lab 03</option>
                    <option value="lab-04">Lab 04</option>
                </select>
            </div>

            {error && <div style={{ color: 'red', marginBottom: '20px' }}>Error: {error}</div>}
            {loading && <div>Loading data...</div>}

            {!loading && !error && (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px' }}>
                    <div style={{ border: '1px solid #eee', padding: '15px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
                        <h3 style={{ textAlign: 'center' }}>Score Distribution</h3>
                        {/* Отрисовка canvas элемента через Chart.js */}
                        <Bar data={barData} />
                    </div>

                    <div style={{ border: '1px solid #eee', padding: '15px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
                        <h3 style={{ textAlign: 'center' }}>Submissions Timeline</h3>
                        <Line data={lineData} />
                    </div>

                    <div style={{ gridColumn: '1 / -1', border: '1px solid #eee', padding: '15px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
                        <h3 style={{ textAlign: 'center' }}>Task Pass Rates</h3>
                        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
                            <thead>
                                <tr style={{ backgroundColor: '#f9f9f9', borderBottom: '2px solid #ddd', textAlign: 'left' }}>
                                    <th style={{ padding: '12px 8px' }}>Task</th>
                                    <th style={{ padding: '12px 8px' }}>Average Score</th>
                                    <th style={{ padding: '12px 8px' }}>Total Attempts</th>
                                </tr>
                            </thead>
                            <tbody>
                                {passRates.map((pr) => (
                                    <tr key={pr.task} style={{ borderBottom: '1px solid #eee' }}>
                                        <td style={{ padding: '12px 8px' }}>{pr.task}</td>
                                        <td style={{ padding: '12px 8px' }}>{pr.avg_score}%</td>
                                        <td style={{ padding: '12px 8px' }}>{pr.attempts}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
}