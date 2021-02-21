import Container from '@material-ui/core/Container';
import { Route } from 'react-router-dom';

import Appbar from './components/Appbar';
import ProjectList from './containers/ProjectList';
import ProjectForm from './components/ProjectForm';
import ProjectDetail from './containers/ProjectDetail';
import './App.css';

function App() {
  return [
    <Appbar />,
    <Container>
      <Route path="/:id" component={ProjectDetail} />
      <Route exact path="/" component={ProjectList} />

      {/* <ProjectDetail /> */}
    </Container>
  ];
}

export default App;
