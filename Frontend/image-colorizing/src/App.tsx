import React from 'react';
import ImageHandler from "./ImageHandler";
import {SnackbarProvider, useSnackbar} from 'notistack';

function App() {
  return (
    <div>
        <SnackbarProvider maxSnack={3}>
            <ImageHandler/>
        </SnackbarProvider>
    </div>
  );
}

export default App;
