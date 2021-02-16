import React, { useState } from 'react';
import * as yup from 'yup';
import { useForm, useFieldArray } from 'react-hook-form';
import { Typography, Grid, Button, CssBaseline } from '@material-ui/core';

import NodeFields from './NodeFields';
import FormikForm from '../UI/Form/FormikForm';

const projectControls = [
  {
    controltype: 'input',
    name: 'Name',
    placeholder: 'Name',
    errorLabel: true
  }
];
const projectSchema = yup.object().shape({
  Name: yup.string().required()
});

const ProjectForm = (props) => {
  const [ fileName, setFileName ] = useState('Upload');
  const [ formError, setFormError ] = useState(false);
  const [ submitDisabled, setSubmitDisabled ] = useState(false);
  const [ saving, setSaving ] = useState(false);
  const [ fileText, setFileText ] = useState('');
  const { register, handleSubmit, control } = useForm();
  const { fields, append, remove } = useFieldArray({
    control,
    name: 'nodes'
  });
  const [ nodes, setNodes ] = useState([]);

  const fileUploadChanged = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      const fileReader = new FileReader();
      fileReader.readAsText(file);
      fileReader.onload = async (e) => {
        const text = e.target.result;
        setFileText(text);
      };
    }
  };
  const formCancelled = () => {
    setFileText('');
    setFileName('Upload');
    props.cancelled();
  };
  // it means that form is submitted and saved succesfully
  // if (props.saved) {
  //   setFileText('');
  //   setFileName('Upload');
  //   setSubmitDisabled(false);
  // }
  if (props.formSubmitErrors && submitDisabled) {
    setSubmitDisabled(false);
  }

  const formSubmitHandler = (values) => {
    if (!(nodes.length && fileName && fileText)) {
      setFormError(true);
    } else {
      const obj = {
        worker_nodes: [ ...nodes ],
        name: values.Name,
        initial_config: JSON.parse(fileText)
      };
      props.submitted(obj);
      setSubmitDisabled(true);
      setFormError(false);
    }
  };

  const submitNodesHandler = (fields) => {
    setSaving(true);
    setNodes(fields.nodes);
  };
  const appendNode = (field) => {
    setSaving(false);
    append(field);
  };

  return (
    <div style={{ padding: 16, margin: 'auto', maxWidth: 600 }}>
      <CssBaseline />
      <Typography variant="h4" align="center" component="h1" gutterBottom>
        Smart Horizontal and Vertical Scaling Application
      </Typography>
      <Typography variant="h5" align="center" component="h2" gutterBottom>
        Open-Api-Based Configurations
      </Typography>
      <Grid item xs={12}>
        <input
          accept="application/JSON"
          hidden
          id="raised-button-file"
          type="file"
          required
          onChange={fileUploadChanged}
        />
        <label htmlFor="raised-button-file">
          <Button variant="raised" component="span">
            {fileName}
          </Button>
        </label>
        {props.fileError && <small>config file is required.</small>}
      </Grid>
      <FormikForm
        submitDisabled={submitDisabled}
        controls={projectControls}
        schema={projectSchema}
        submitted={formSubmitHandler}
        cancelled={formCancelled}
        invalidForm={formError}
        formErrors={props.formSubmitErrors}
      />
      <form onSubmit={handleSubmit(submitNodesHandler)}>
        <NodeFields
          append={appendNode}
          fields={fields}
          register={register}
          control={control}
          remove={remove}
          isSaving={saving}
        />
      </form>
      <pre>{fileText}</pre>
    </div>
  );
};

export default ProjectForm;
