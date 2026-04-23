import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Wallet, ArrowUpRight, ArrowDownLeft, BarChart3 } from 'lucide-react';

function App() {
  // 1. State: This is the memory of your app
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  // 2. Fetch Logic: Calling your FastAPI server
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/transactions');
        setTransactions(response.data.transactions);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 p-8">
      {/* Header Area */}
      <header className="flex justify-between items-center mb-12">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <Wallet className="text-emerald-400" /> Fin-Flow
          </h1>
          <p className="text-slate-400">AI-Powered Financial Insights</p>
        </div>
        <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
          <span className="text-sm text-slate-400">System Status:</span>
          <span className="ml-2 text-emerald-400 font-mono text-sm">ONLINE</span>
        </div>
      </header>

      {/* Main Dashboard Grid */}
      <main className="max-w-6xl mx-auto">
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-emerald-400"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6">
            {/* Transaction List Card */}
            <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">
              <div className="p-6 border-b border-slate-800 flex justify-between items-center">
                <h2 className="text-xl font-semibold">Recent Transactions</h2>
                <BarChart3 className="text-slate-500" size={20} />
              </div>
              
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="bg-slate-900/50 text-slate-400 text-sm">
                      <th className="p-4 font-medium">Date</th>
                      <th className="p-4 font-medium">Description</th>
                      <th className="p-4 font-medium">Category</th>
                      <th className="p-4 font-medium text-right">Amount</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800">
                    {transactions.map((t, index) => (
                      <tr key={index} className="hover:bg-slate-800/40 transition-colors">
                        <td className="p-4 text-sm text-slate-300">{t.date}</td>
                        <td className="p-4 font-medium">{t.description}</td>
                        <td className="p-4">
                          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                            {t.category}
                          </span>
                        </td>
                        <td className="p-4 text-right font-mono font-semibold">
                          ${t.amount.toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;