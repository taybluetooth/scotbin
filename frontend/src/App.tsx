import { useEffect, useState } from "react";

type BinColorMapping = {
  [key: string]: "green" | "grey";
};

function App() {
  // State to store the fetched data
  const [calendar, setCalendar] = useState<BinColorMapping | null>(null);
  // Fetch data from FastAPI on component mount
  useEffect(() => {
    fetch("http://localhost:8000/calendar/edinburgh/Provost%20Haugh") // FastAPI endpoint URL
      .then((response) => response.json()) // Parse the JSON response
      .then((data) => setCalendar(JSON.parse(data))) // Set the data in the state
      .catch((error) => console.error("Error fetching data: ", error));
  }, []); // Empty dependency array, so it runs only once on mount

  return (
    <div className="App">
      <h1>FastAPI + React Example</h1>

      {calendar ? (
        <div>
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Color</th>
              </tr>
            </thead>
            <tbody>
            {Object.entries(calendar).map(([date, color]) => (
                <tr key={date}>
                  <td>{date}</td>
                  <td>{color}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>Loading data...</p>
      )}
    </div>
  );
}

export default App;
