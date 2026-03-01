import SetupPage from "./pages/SetupPage";
import Dashboard from "./pages/Dashboard";
import DbDiagPage from "./pages/dbDiagPage";
import DbhealthPage from "./pages/dBHealthPage";
import DbperfPage from "./pages/dBperfPage";
import DbSummaryPage from "./pages/dbSummaryPage";
import {BrowserRouter,Routes,Route} from "react-router-dom"

import { useAppContext } from "./context/AppContext";
import Layout from "./pages/Layout";

function App() {
  const { isConfigured } = useAppContext();

  // return isConfigured ? <Dashboard /> : <SetupPage />;
  return(

    <BrowserRouter>
    <Routes>
      <Route element={<Layout/>}>
<Route path="/" element={<Dashboard/>}/>
<Route path="/health" element={<DbhealthPage/>}/>
<Route path="/performance" element={<DbperfPage/>}/>
<Route path="/dbsummary" element={<DbSummaryPage/>}/>
<Route path="/diaglog" element={<DbDiagPage/>}/>
</Route>
    </Routes>
    </BrowserRouter>
  );
  // <p>This is app</p>
}

export default App;


