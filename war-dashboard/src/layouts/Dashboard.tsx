import React, { ReactElement } from "react";
import { useStyles } from "themes/DynamicDrawerTheme";
import axios from "axios";
import buffer from "buffer";
import crypto from "crypto";

interface Props {}

const publicKey =
  "-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAtY8PYxFCW+3YT/Sg8gBz\ny0lB2l48yqMnNkvn94pVGE/EH4+FlrV0hMUDnO3pZVmJ2tKayCIQ91v28TlS+3Fy\nJ0Zk7gVeQzELcBbQPmIzEvw27TJRNw/W1OnLOZb4+rzZdN24JS3hAlQcDcHToYWC\nERpifLqgf0JNIqg8FxBxikunvjZuGTTNWO3ZCrPCqG/gRVJr29KrSG2+cg1UzMLk\n3w6Jqu6qPlZfka6nfgXEUXV0qSCU0ek4er3Gvr/qQocKpQVdZdCaeKC/v23tWnP6\nLZ6WbO+KtVSmo1JGCXqQ6WBUcd7oDCQI6k+Htl/alNsxNVUSb5DmboYmbDdot7hV\nvu2XzhNgAW1ZW9N2FaCaxJpKPbqIIDQYj+jQ/J/IIK6OKfCglYD12mgQ01rNMyBN\n277+Cs8mLMcS+Ufe597xy1sKBU7EKKoWMXs7mM4/C5LwP27gP24SfjBAAIgMgXsW\nz7zE0vuDVXUvCsQAb8bta6gbmeJpcEZbf4A1iPKf7qpMPHqKfGp57woa1FQirL+k\nAlEJ0Dob1T4l7yPRxNDdPuSTd4Bl9gQx8GodS4ZZBBrlAyA0+IL+WZMbSiqm1EYS\nLpkWZQFHvtP0c64OYjpDXf5t5Pg/iaDcNmAqsVNamfg6CFobqHO+aB0cyvlbiI3R\nhSezJnelEBJrr2U/nM22+i0CAwEAAQ==\n-----END PUBLIC KEY-----\n";

export default function Dashboard({}: Props): ReactElement {
  const [machineNameData, setMachineNameData] = React.useState({} as any);
  React.useEffect(() => {
    async function fetchData() {
      await axios
        .post(
          "https://ytp3g6j58c.execute-api.us-east-2.amazonaws.com/test/get-machine-name"
        )
        .then((response) => {
          if (response.data.success) {
            setMachineNameData(response.data.data);
          }
        });
    }

    fetchData();
    if (machineNameData) {
      let machineBuffer = machineNameData.machine_name;
      let plaintext = crypto.publicDecrypt(publicKey, machineBuffer);
      console.log(plaintext.toString("utf8"));
    }
  }, [machineNameData]);

  return (
    <div>
      <h1>Dashboard Header</h1>
    </div>
  );
}
