import logs from "../data/logs";

const Logs = () => {
    return (
        <div>
            <h1>Logs</h1>
            <ol>
                {logs.map((log) => (
                    <li key={log.id}>
                        {log.activity}: {log.carbon} kg CO2
                    </li>
                ))}
            </ol>
        </div>
    )
}

export default Logs;