import { ChangeEvent, useEffect, useState } from "react";

type BinColorMapping = {
  [key: string]: "green" | "grey";
};

// Define the type for your street data
type StreetData = {
  [key: string]: string[];
};

function App() {
  // State to store the fetched data
  const [calendar, setCalendar] = useState<BinColorMapping | null>(null);
  const [edinStreets, setEdinStreets] = useState<StreetData>({});
  const [loading, setLoading] = useState(false);
  const [selectedStreet, setSelectedStreet] = useState("");

  const [input, setInput] = useState<string>(""); // User input
  const [suggestions, setSuggestions] = useState<string[]>([]); // Filtered suggestions

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value.toLowerCase();
    setInput(value);
  
    if (value.length === 0) {
      setSuggestions([]); // Clear suggestions if input is empty
    } else {
      // Flatten all street names into a single array
      const allStreets = Object.values(edinStreets).flat();
      
      // Filter streets that contain the input value
      const matches = allStreets.filter((street) =>
        street.toLowerCase().includes(value)
      );
      
      setSuggestions(matches);
    }
  };

  const ensureUniqueStreetData = (data: StreetData): StreetData => {
    const uniqueData: StreetData = {};

    for (const [key, value] of Object.entries(data)) {
      uniqueData[key] = Array.from(new Set(value)); // Remove duplicates for each array
    }

    return uniqueData;
  };

  const handleClick = (street: string) => {
    setLoading(true);
    setSelectedStreet(street.replace(" ", "%20"));
  };

  useEffect(() => {
    const getEdinStreetNames = async () => {
      try {
        const response = await fetch(
          "https://raw.githubusercontent.com/taybluetooth/scotbin/refs/heads/main/backend/app/data/edin_streets.json"
        );
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        const uniqueStreetData = ensureUniqueStreetData(data);
        setEdinStreets(uniqueStreetData);
      } catch (error) {
        console.error("Error fetching JSON data:", error);
      }
    };
  
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
      <div style={{ margin: "20px" }}>
        <input
          type="text"
          placeholder="Search streets..."
          value={input}
          onChange={handleChange}
          style={{
            padding: "10px",
            width: "300px",
            border: "1px solid #ccc",
            borderRadius: "4px",
          }}
        />
        {suggestions.length > 0 && (
          <ul
            style={{ marginTop: "10px", listStyleType: "none", padding: "0" }}
          >
            {suggestions.map((street, index) => (
              <button
                onClick={() => handleClick(street)}
                key={`select-street-btn-${street}-${index}`}
                style={{
                  padding: "10px",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                  backgroundColor: "#000000",
                  marginBottom: "5px",
                }}
              >
                {street}
              </button>
            ))}
          </ul>
        )}
      </div>
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
