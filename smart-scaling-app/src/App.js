import Container from '@material-ui/core/Container';

import Appbar from './components/Appbar';
import ProjectList from './containers/ProjectList';
import './App.css';

function App() {
  return [
    <Appbar />,
    <Container>
      <ProjectList />
    </Container>
  ];
}

export default App;
