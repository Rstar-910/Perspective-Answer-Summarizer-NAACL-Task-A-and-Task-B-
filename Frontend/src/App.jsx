import React, { useState } from "react";
import axios from "axios";
import { HeartPulse, Send, Loader2 } from "lucide-react";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResults(null);

    try {
      const response = await axios.post("http://localhost:5000/api/process-question", {
        question,
        answer,
      });
      setResults(response.data);
    } catch (error) {
      console.error("Error processing question:", error);
      alert("An error occurred while processing your request.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-gray-200 flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-4xl bg-gray-800 shadow-2xl rounded-3xl overflow-hidden">
        <header className="bg-gradient-to-r from-purple-700 to-purple-900 text-white p-8 flex items-center shadow-lg">
          <HeartPulse className="mr-4 w-14 h-14 text-white" />
          <h1 className="text-4xl font-extrabold tracking-tight leading-tight">
            Perspective Answer Summarizer
          </h1>
        </header>

        <main className="p-10">
          <form onSubmit={handleSubmit} className="space-y-8 bg-gray-700 p-10 rounded-lg shadow-md">
            <div>
              <label htmlFor="question" className="block text-lg font-semibold text-gray-300 mb-3">
                Question
              </label>
              <textarea
                id="question"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Enter your question here"
                required
                className="w-full p-4 border border-gray-600 rounded-lg bg-gray-800 text-gray-200 focus:ring-4 focus:ring-purple-500 focus:outline-none transition-all duration-300 ease-in-out"
                rows="4"
              />
            </div>

            <div>
              <label htmlFor="answer" className="block text-lg font-semibold text-gray-300 mb-3">
                Answer
              </label>
              <textarea
                id="answer"
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="Enter the answer text here"
                required
                className="w-full p-4 border border-gray-600 rounded-lg bg-gray-800 text-gray-200 focus:ring-4 focus:ring-purple-500 focus:outline-none transition-all duration-300 ease-in-out"
                rows="4"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center bg-gradient-to-r from-green-600 to-blue-700 text-white py-4 rounded-lg hover:opacity-90 transition-all duration-300 ease-in-out disabled:opacity-50 shadow-lg"
            >
              {loading ? (
                <><Loader2 className="mr-2 animate-spin" /> Processing...</>
              ) : (
                <><Send className="mr-2" /> Submit</>
              )}
            </button>
          </form>

          {results && (
            <div className="mt-10 bg-gray-700 p-8 rounded-lg shadow-inner">
              <h2 className="text-3xl font-bold text-gray-200 mb-8">Results</h2>

              <div className="grid md:grid-cols-2 gap-8">
                <div>
                  <h3 className="text-xl font-semibold text-gray-300 mb-5">Extracted Spans</h3>
                  <ul className="space-y-4">
                    {results.spans.map((span, index) => (
                      <li
                        key={index}
                        className="bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-600"
                      >
                        <strong className="text-purple-400">{span.category}:</strong> {span.text}
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-gray-300 mb-5">Summaries</h3>
                  <div className="space-y-6">
                    {[
                      { label: "Information Summary", key: "information_summary" },
                      { label: "Cause Summary", key: "cause_summary" },
                      { label: "Experience Summary", key: "experience_summary" },
                      { label: "Suggestion Summary", key: "suggestion_summary" }
                    ].map(({ label, key }) => (
                      <div
                        key={key}
                        className="bg-gray-800 p-5 rounded-lg shadow-sm border border-gray-600"
                      >
                        <strong className="block text-purple-400 mb-3">{label}:</strong>
                        <p className="text-gray-200">{results[key]}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;