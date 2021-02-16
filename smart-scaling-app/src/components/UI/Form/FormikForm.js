import React from 'react';
import { Button, makeStyles, Typography } from '@material-ui/core';
import { Formik, Form } from 'formik';
import PropTypes from 'prop-types';

import FormikField from '../Control/FormikField';

const FormikForm = (props) => {
  const classes = useStyles();
  const { formErrors } = props;

  return (
    <div>
      <Formik
        initialValues={{}}
        validationSchema={props.schema}
        onSubmit={(values) => {
          props.submitted(values);
        }}
        onReset={() => {
          props.cancelled();
        }}
      >
        {({ errors, touched }) => (
          <Form className={classes.Form}>
            <Typography variant="h5" align="center">
              {props.title}
            </Typography>
            {formErrors && <div className={classes.ErrorText}>{formErrors.map((err) => <p>{err}</p>)}</div>}
            {props.invalidForm && <p className={classes.ErrorText}>Please add atleast 1 Node and upload config.</p>}
            {props.controls.map((control) => {
              return (
                <FormikField
                  key={control.name}
                  className={classes.Control}
                  errors={touched[control.name] ? errors[control.name] : null}
                  {...control}
                />
              );
            })}
            <br />
            <Button
              className={classes.Control}
              type="submit"
              variant="contained"
              color="primary"
              disabled={props.submitDisabled}
            >
              Submit
            </Button>
            <Button variant="contained" type="reset">
              Cancel
            </Button>
          </Form>
        )}
      </Formik>
    </div>
  );
};

FormikForm.propTypes = {
  controls: PropTypes.array.isRequired,
  schema: PropTypes.object.isRequired
};

export default FormikForm;

const useStyles = makeStyles(() => ({
  Form: {
    margin: 'auto',
    width: '600px'
  },
  Control: {
    margin: '10px'
  },
  ErrorText: {
    color: 'red'
  }
}));
