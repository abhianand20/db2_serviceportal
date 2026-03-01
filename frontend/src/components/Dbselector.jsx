import { useAppContext } from "../context/AppContext";

function DbSelector() {
  const { dbName, setDbName } = useAppContext();

  return (
    <div>
      <label>Select Database:</label>
      <select value={dbName} onChange={(e) => setDbName(e.target.value)}>
        <option value="testdb">testdb</option>
        <option value="proddb">proddb</option>
      </select>
    </div>
  );
}

export default DbSelector;
