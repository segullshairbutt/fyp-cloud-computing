import React, { useState } from 'react';
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';

import ConfirmationDialog from '../UI/ConfirmationDialog';
import Dialog from '../UI/Dialog';
import ProjectForm from '../ProjectForm';
import ProjectTable from './ProjectTable';
import Aux from '../hoc/Auxx';

const useRowStyles = makeStyles({
  root: {
    '& > *': {
      borderBottom: 'unset'
    }
  },
  addButtonStyle: {
    marginLeft: '10px'
  }
});

const ProjectList = (props) => {
  const classes = useRowStyles();
  const [ deleteProject, setDeleteProject ] = useState(false);
  const [ projectForm, setProjectForm ] = useState(false);
  let formTitle = 'Project Form';

  const disagreed = () => {
    setDeleteProject(false);
  };

  const formCancelled = () => {
    setProjectForm(false);
    props.cancelClicked();
  };

  return (
    <Aux>
      <Typography variant="h2" align="center">
        Project List
        <Button className={classes.addButtonStyle} size="small" color="secondary" onClick={() => setProjectForm(true)}>
          Add New
        </Button>
      </Typography>
      <ConfirmationDialog open={deleteProject} disagreed={disagreed} />
      <Dialog open={projectForm} title={formTitle} hideActions size="lg">
        {projectForm && (
          <ProjectForm
            submitted={props.formSubmitted}
            cancelled={formCancelled}
            text={props.fileText}
            formSubmitErrors={props.submitErrors}
            formSaved={props.saved}
          />
        )}
      </Dialog>
      <ProjectTable
        projects={props.projects}
        showProjectForm={() => setProjectForm(true)}
        showDeleteProject={() => setDeleteProject(true)}
      />
    </Aux>
  );
};

export default ProjectList;
