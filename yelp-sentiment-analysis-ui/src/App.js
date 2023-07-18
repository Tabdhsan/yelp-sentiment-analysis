import React, { useState } from 'react';
import { Box, Typography, TextField, Button, CircularProgress, Stack } from '@mui/material';

function App() {
  const [firstUrl, setFirstUrl] = useState('');
  const [secondUrl, setSecondUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const [url1Graph, setUrl1Graph] = useState('')
  const [url2Graph, setUrl2Graph] = useState('')
  const [gptBlurb, setGptBlurb] = useState('')
  const [dataLoaded, setDataLoaded] = useState(false)


  const handleSubmit = async (e) => {
    e.preventDefault();
    setDataLoaded(false)

    // Start loading animation
    setLoading(true);

    fetch(`http://localhost:5000/getGraph?url1=${firstUrl}&url2=${secondUrl}`, {
      headers: {
        'Access-Control-Allow-Origin': '*'
      }
    })
      .then(response => response.json())
      .then(res => {
        console.log('success', res)
        console.log('data.graph', res.data.graph)
        setUrl1Graph(`data:image/png;base64,${res.data.url1GraphImage}`)
        setUrl2Graph(`data:image/png;base64,${res.data.url2GraphImage}`)
        setGptBlurb(res.data.gptBlurb)
        setDataLoaded(true)

      })
      .catch(error => {
        // Handle the error
        console.log('error', error)
      });

    // Stop loading animation
    setLoading(false);

    // Clear the input field
    // setUrl('');
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', fontFamily: 'Arial, sans-serif' }}>
      <Typography variant="h2" sx={{ marginBottom: '1rem' }}>Compare Yelp Ratings</Typography>
      <Typography variant="h4" sx={{ marginBottom: '1rem' }}>
        Please Enter Two Yelp URLs
      </Typography>
      <Stack direction='row'>
        <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', alignItems: 'center' }} disabled={loading}>
          <TextField
            type="text"
            label="Enter URL 1"
            variant="outlined"
            onChange={(e) => setFirstUrl(e.target.value)}
            sx={{ marginRight: '0.5rem' }}
            values={firstUrl}
          />
          <TextField
            type="text"
            label="Enter URL 2"
            variant="outlined"
            onChange={(e) => setSecondUrl(e.target.value)}
            sx={{ marginRight: '0.5rem' }}
            value={secondUrl}
          />
          <Button type="submit" variant="contained" sx={{ backgroundColor: '#007bff', color: '#fff', height: 'fit-content', py: 1 }}>
            Submit
          </Button>
        </Box>
      </Stack>
      {dataLoaded &&
        <>
          <Stack direction='row'>
            <Stack>
              <img src={url1Graph} alt="Graph" />
            </Stack>

            <Stack>
              <img src={url2Graph} alt="Graph2" />
            </Stack>
          </Stack>
          <Typography>{gptBlurb}</Typography>
        </>
      }
      {loading && <CircularProgress sx={{ marginTop: '1rem' }} />}
    </Box >
  );
}

export default App;

// https://www.yelp.com/biz/belly-cake-bayside?osq=Pancakes
// https://www.yelp.com/biz/dtut-new-york?osq=dtut