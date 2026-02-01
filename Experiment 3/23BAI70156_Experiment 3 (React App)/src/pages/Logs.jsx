import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchLogs } from "../store/logSlice";


const Logs = () => {
    const dispatch = useDispatch();
    const {data, status, error} = useSelector((state) => state.logs);
    
    const handleRefresh = () => {
        dispatch(fetchLogs());
    }

    useEffect(() => {
        if(status === "idle") {
            dispatch(fetchLogs());
        }
    }, [status, dispatch]);
    if(status === "loading") {
        return <p>Loading Logs...</p>
    }
    if(status === "failed") {
        return <p>Error : {error}</p>
    }

    return (
        <div>
            <h1>Logs</h1>
            <ol>
                {data.map((log) => (
                    <li key={log.id}>
                        {log.activity}: {log.carbon} kg CO2
                    </li>
                ))}
            </ol>
            <button onClick={handleRefresh}>Refresh</button>
        </div>
    )
}

export default Logs;