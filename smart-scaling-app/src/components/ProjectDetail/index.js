import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import { Button, Container, Typography } from '@material-ui/core';

import TreeView from './TreeView';
import ConfirmationDialog from '../UI/ConfirmationDialog';

const Details = (props) => {
  return (
    <Container>
      <Typography align="left" variant="h2">
        {props.name}
      </Typography>
      <Typography align="left" variant="h4">
        User: {props.username}
      </Typography>
      <Grid container spacing={1}>
        <Grid item xs={6}>
          <Typography align="left" variant="h6">
            Status: {props.status}
          </Typography>
        </Grid>
        <Grid item xs={3}>
          {props.status !== 'Started' && (
            <Button variant="contained" color="primary" onClick={props.started} disabled={props.buttonsDisabled}>
              Start Now
            </Button>
          )}
        </Grid>
        <Grid item xs={3}>
          <Button variant="contained" color="secondary" onClick={props.deleted} disabled={props.buttonsDisabled}>
            Delete
          </Button>
        </Grid>
      </Grid>
    </Container>
  );
};

const createNodes = (config) => {
  let rootId = 1;
  const rootNode = { name: 'main', id: rootId++, children: [] };

  Object.keys(config).forEach((key1) => {
    const obj1 = { name: key1 + '', id: rootId++, children: [] };
    const firstLevelObject = config[key1];

    if (Object.keys(firstLevelObject).length) {
      Object.keys(firstLevelObject).forEach((key2) => {
        const obj2 = { name: key2 + '', id: rootId++, children: [] };
        obj1.children.push(obj2);

        const secondLevelObject = firstLevelObject[key2];
        if (typeof secondLevelObject === 'string') {
          obj2.children.push({ name: secondLevelObject, id: rootId++ });
        } else if (Object.keys(secondLevelObject).length) {
          Object.keys(secondLevelObject).forEach((key3) => {
            const obj3 = { name: key3 + '', id: rootId++, children: [] };
            obj2.children.push(obj3);

            const thirdLevelObject = secondLevelObject[key3];
            if (typeof thirdLevelObject === 'string') {
              obj3.children.push({ name: thirdLevelObject, id: rootId++ });
            } else if (Object.keys(thirdLevelObject).length) {
              Object.keys(thirdLevelObject).forEach((key4) => {
                const obj4 = { name: key4 + '', id: rootId++, children: [] };
                obj3.children.push(obj4);

                const fourthLevelObject = thirdLevelObject[key4];
                if (typeof fourthLevelObject === 'string') {
                  obj4.children.push({ name: fourthLevelObject, id: rootId++ });
                } else
                  Object.keys(fourthLevelObject).length &&
                    Object.keys(fourthLevelObject).forEach((key5) => {
                      const obj5 = { name: key5 + '', id: rootId++, children: [] };
                      obj4.children.push(obj5);

                      const fifthLevelObject = fourthLevelObject[key5];
                      if (typeof fifthLevelObject === 'string') {
                        obj5.children.push({ name: fifthLevelObject, id: rootId++ });
                      } else
                        Object.keys(fifthLevelObject).length &&
                          Object.keys(fifthLevelObject).forEach((key6) => {
                            const obj6 = { name: key6 + '', id: rootId++, children: [] };
                            obj5.children.push(obj6);

                            const sixthLevelObject = fifthLevelObject[key6];
                            if (typeof sixthLevelObject === 'string') {
                              obj6.children.push({ name: sixthLevelObject, id: rootId++ });
                            } else
                              Object.keys(sixthLevelObject).length &&
                                Object.keys(sixthLevelObject).forEach((key7) => {
                                  const obj7 = { name: key7 + '', id: rootId++, children: [] };
                                  obj6.children.push(obj7);

                                  const seventhLevelObject = sixthLevelObject['key7'];
                                  if (typeof seventhLevelObject === 'string') {
                                    obj7.children.push({ name: seventhLevelObject, id: rootId++ });
                                  } else
                                    seventhLevelObject &&
                                      Object.keys(seventhLevelObject).length &&
                                      Object.keys(seventhLevelObject).forEach((key8) => {
                                        const obj8 = { name: key8, id: rootId++ };
                                        obj7.children.push(obj8);
                                      });
                                });
                          });
                    });
              });
            }
          });
        }
      });
    }
    rootNode.children.push(obj1);
  });

  return rootNode;
};

export default function ProjectDetails(props) {
  const classes = useStyles();
  const { config } = props.project;
  const [ open, setOpen ] = useState(false);

  let nodes = [];
  let status = 'Not Started';
  if (config) {
    status = 'Started';
    const { code } = config;
    const newConfig = { clusters: code.info['x-clusters'], schemas: code.schemas };
    nodes = createNodes(newConfig);
  }

  const agreed = () => {
    setOpen(false);
    props.projectDeleted();
  };
  const disAgreed = () => {
    setOpen(false);
  };

  return (
    <div className={classes.root}>
      <Grid container spacing={3}>
        <Grid item xs={6}>
          <Paper className={classes.paper}>
            <ConfirmationDialog open={open} disagreed={disAgreed} agreed={agreed} />
            <Details
              name={props.projectName}
              status={status}
              username={props.user}
              buttonsDisabled={props.buttonsDisabled}
              started={props.projectStarted}
              deleted={() => setOpen(true)}
            />
          </Paper>
        </Grid>
        <Grid item xs={6}>
          <Paper className={classes.paper}>
            <Grid item xs zeroMinWidth>
              <TreeView node={nodes} />
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
}

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
    height: 'auto'
  }
}));
