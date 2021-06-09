import { useState, useEffect } from 'react';
import SwaggerUI from 'swagger-ui-react';
import 'swagger-ui-react/swagger-ui.css';

import axios from '../../store/custom-axios';

const Swagger = (props) => {
  const [ spec, setSpec ] = useState(null);
  const [ error, setError ] = useState(new Error('LOADING'));

  useEffect(() => {
    const { id, filename } = props.match.params;
    if (!(id && filename)) {
      setError(new Error('unable to load config'));
    } else {
      axios.get(`/api/projects/${id}/config/${filename}`).then((res) => {
        setSpec(res.data);
        setError(null);
        debugger;
      });
    }
  }, []);

  return error ? <div>{error.message}</div> : <SwaggerUI spec={spec} />;
};

export default Swagger;
