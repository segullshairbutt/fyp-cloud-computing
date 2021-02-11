import { useState } from 'react';
import HomeComponent from '../components/Home';

const Home = (props) => {
  const [ fileName, setFileName ] = useState('Upload');
  const [ fileText, setFileText ] = useState('');
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
  const formSubmitHandler = (e) => {
    e.preventDefault();
  };

  return (
    <HomeComponent
      fileUploaded={fileUploadChanged}
      fileName={fileName}
      formSubmitted={formSubmitHandler}
      text={fileText}
    />
  );
};

export default Home;
