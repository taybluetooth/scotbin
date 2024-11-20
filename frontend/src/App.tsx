import { useEffect, useState } from "react";
import Papa from "papaparse";

type BinColorMapping = {
  [key: string]: "green" | "grey";
};

function App() {
  // State to store the fetched data
  const [calendar, setCalendar] = useState<BinColorMapping | null>(null);
  const [edinStreets, setEdinStreets] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedStreet, setSelectedStreet] = useState<string | null>(null);

  const getEdinStreetNames = () => {
    Papa.parse<string[]>(
      "https://raw.githubusercontent.com/taybluetooth/scotbin/main/backend/app/data/edin_streets.csv",
      {
        download: true,
        header: false,
        skipEmptyLines: true,
        complete: (results) => {
          const streets = results.data.map((row) => row[0]);
          const streetsSet = Array.from(new Set(streets));
          setEdinStreets(streetsSet);
        },
        error: (error) => console.error("Error downloading CSV:", error),
      }
    );
  };

  const onChange = (e: React.FormEvent<HTMLSelectElement>) => {
    setLoading(true);
    setSelectedStreet(e.currentTarget.value.replace(" ", "%20"));
  };

  useEffect(() => {
    getEdinStreetNames();
  }, []);

  useEffect(() => {
    if (!selectedStreet) return;

    fetch(`http://localhost:8000/calendar/edinburgh/${selectedStreet}`)
      .then((response) => response.json())
      .then((data) => {
        setCalendar(JSON.parse(data));
        setLoading(false);
      })
      .catch((error) => console.error("Error fetching data: ", error));
  }, [selectedStreet]);

  return (
    <div className="App">
      <h1>Scotbin</h1>
      <label htmlFor="edinburgh-street-dropdown">Select a Street:</label>
      <select id="edinburgh-street-dropdown" onChange={onChange}>
        <option value="">Select a street</option>
        {edinStreets.map((street) => (
          <option key={`edinburgh-street-${street}`} value={street}>
            {street}
          </option>
        ))}
      </select>
      {!calendar && !loading && <p>Please select a street</p>}
      {loading && <p>Loading data...</p>}
      {!loading && calendar && (
        <table>
          <thead>
            <tr>
              <th>Dates</th>
              <th>Bin</th>
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
      )}
    </div>
  );
}

export default App;
