import React, { useState, useEffect, useMemo, useCallback } from 'react';
import axios from 'axios';
import { Wallet, ArrowUpRight, ArrowDownLeft, BarChart3, TrendingDown } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

// Colors for a high-fidelity look
const COLORS = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4'];

const FileUpload = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    try {
      await axios.post('http://127.0.0.1:8000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      onUploadSuccess(); // Refresh the data list
    } catch (error) {
      alert("upload failed: " + error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-slate-900 border-2 border-dashed border-slate-700 rounded-2xl p-8 text-center hover:border-emerald-500 transition-colors group cursor-pointer relative">
      <input
        type="file"
        onChange={handleFileChange}
        className="absolute inset-0 opacity-0 cursor-pointer"
      />
      <div className="flex flex-col items-center gap-2">
        <div className="p-3 bg-slate-800 rounded-full group-hover:bg-emerald-500/20 group-hover:text-emerald-400 transition-colors">
          {uploading ? <div className="animate-spin h-6 w-6 border-2 border-t-transparent border-emerald-400 rounded-full" /> : "📁"}
        </div>
        <p className="text-slate-300 font-medium">Click or drag bank statement (CSV)</p>
        <p className="text-slate-500 text-xs text-uppercase tracking-widest">Max size: 5MB</p>
      </div>
    </div>
  );
};

function App() {
  // 1. State: This is the memory of my app
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/transactions');
      setTransactions(response.data.transactions);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching data:", error);
      setLoading(false);
    }
  }, []); // The Empty array means this function only get created once

  const handleClearData = async () => {
    if (window.confirm("Are you sure you want to delete all transaction history?")) {
      try {
        await axios.delete('http://127.0.0.1:8000/clear-data');
        setTransactions([]); // Clear UI immediately
        alert("Database reset successfully.");
      } catch (error) {
        alert("Failed to clear data: " + error.message);
      }
    }
  };

  useEffect(() => {
    fetchData();
  }, [fetchData]);

// Calculate totals and group data for the chart
const { totalSpent, chartData } = useMemo(() => {
  const total = transactions.reduce((acc, curr) => acc + curr.amount, 0);

  // Group by category
  const grouped = transactions.reduce((acc, curr) => {
    acc[curr.category] = (acc[curr.category] || 0) + curr.amount;
    return acc;
  }, {});

  // Recharts
  const formattedData = Object.keys(grouped).map(key => ({
    name: key,
    value: parseFloat(grouped[key].toFixed(2))
  }));

  return { totalSpent: total, chartData: formattedData };
}, [transactions]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 p-8">
      {/* Header Area */}
      <header className="flex justify-between items-center mb-10 max-w-6xl mx-auto">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <Wallet className="text-emerald-400" /> Cognis
          </h1>
          <p className="text-slate-400">Advanced financial intelligence</p>
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={handleClearData}
            className="text-xs font-bold text-slate-500 hover:text-red-400 uppercase tracking-widest transition-colors border border-slate-800 hover:border-red-500/50 px-3 py-2 rounded-lg"
          >
            Clear history
          </button>
        
        <div className="bg-slate-900 px-4 py-2 rounded-xl border border-slate-800 flex items-center gap-3">
          <span className="h-2 w-2 bg-emerald-400 rounded-full animated-pulse"></span>
          <span className="text-sm font-mono text-emerald-400">API CONNECTED</span>
        </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto space-y-8">
        {/* TOP CARDS SECTION */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800">
            <div className="flex items-center gap-3 text-slate-400 mb-2">
              <TrendingDown size={18} />
              <span className="text-sm font-medium uppercase tracking-wider">Total Spending</span>
            </div>
            <div className="text-3xl font-bold">${totalSpent.toFixed(2)}</div>
          </div>

          <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 md:col-span-2 flex items-center justify-between">
            <div className="h-[200px] w-full min-w-0">
              {/* PIE CHART */}
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={chartData}
                    innerRadius={40}
                    outerRadius={60}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} stroke="none" />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }}
                    itemStyle={{ color: '#f8fafc'}}
                  />
                  <Legend iconType="circle" />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="hidden lg:block pr-8">
              <h3 className="text-slate-400 text-sm mb-1 uppercase">Breakdown</h3>
              <p className="text-xs text-slate-500 max-w-[200px]">Visualizing your expenses across {chartData.length} AI-identified categories.</p>
            </div>
          </div>
        </div>

        <div className="mb-8">
          <h3 className="text-slate-400 text-sm mb-4 uppercase tracking-widest">Data Input</h3>
          <FileUpload onUploadSuccess={fetchData} />
        </div>

            {/* Recent transactions table */}
            <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">
              <div className="p-6 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
                <h2 className="text-xl font-semibold">Transactions History</h2>
                <BarChart3 className="text-slate-500" size={20} />
              </div>
              
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="text-slate-500 text-xs uppercase tracking-wider border-b border-slate-800">
                      <th className="p-4 font-medium">Date</th>
                      <th className="p-4 font-medium">Description</th>
                      <th className="p-4 font-medium">Category</th>
                      <th className="p-4 font-medium text-right">Amount</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800">
                    {transactions.map((t, index) => (
                      <tr key={index} className="hover:bg-slate-800/30 transition-colors group">
                        <td className="p-4 text-sm text-slate-400 font-mono">{t.date}</td>
                        <td className="p-4 font-medium text-slate-200">{t.description}</td>
                        <td className="p-4">
                          <span className="px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 backdrop-blur-sm transition-all group-hover:bg-emerald-500/20 group-hover:shadow-[0_0_10px_rgba(52,211,153,0.15)] group-hover:scale-105 inline-block">
                            {t.category}
                          </span>
                        </td>
                        <td className="p-4 text-right font-mono font-bold text-slate-100">
                          ${t.amount.toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
      </main>
    </div>
  );
}

export default App;