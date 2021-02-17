import Container from '@material-ui/core/Container';

import Appbar from './components/Appbar';
import ProjectList from './containers/ProjectList';
import ProjectForm from './components/ProjectForm';
import ProjectDetail from './containers/ProjectDetail';
import './App.css';

function App() {
  return [
    <Appbar />,
    <Container>
      {/* <ProjectList /> */}
      <ProjectDetail />
    </Container>
  ];
}

export default App;
