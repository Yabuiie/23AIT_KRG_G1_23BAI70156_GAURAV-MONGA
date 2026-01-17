import logs from "../data/logs";

const Logs = () => {
    const highCarbon = logs.filter((log) => {
                        return log.carbon > 3;
                    })
    return (
        <div>
            <h1>Logs with Carbon geater than 3</h1>
            <ol>
                {highCarbon.map((log) => (
                    <li key = {log.id}>
                        {log.activity} = {log.carbon} kg CO2
                    </li>
                ))}
            </ol>
        </div>
    )
}

export default Logs;