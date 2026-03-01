import { createContext, useContext, useState } from "react";

const AppContext = createContext();

export function AppProvider({ children }) {
  const [server, setServer] = useState("localhost");
  const [instance, setInstance] = useState("db2inst1");
  const [dbName, setDbName] = useState("testdb");
  const [isConfigured, setIsConfigured] = useState(false);

  function configure(server, instance, dbName) {
    setServer(server);
    setInstance(instance);
    setDbName(dbName);
    setIsConfigured(true);
  }

  return (
    <AppContext.Provider
      value={{
        server,
        instance,
        dbName,
        isConfigured,
        configure
      }}
    >
      {children}
    </AppContext.Provider>
  );
}


export function useAppContext() {
  return useContext(AppContext);
}
