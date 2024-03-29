import React, { useState } from 'react';
import { Box, Button, Stack } from '@mui/material';
import GraphCard from './components/GraphCard';
import InputCard from './components/InputCard';
import Loading from './assets/LoadingToaster.gif';
import { getDetails } from './api';

function App() {
	const [loading, setLoading] = useState(false);
	const [firstUrl, setFirstUrl] = useState('');
	const [secondUrl, setSecondUrl] = useState('');
	const [url1Graph, setUrl1Graph] = useState('');
	const [url2Graph, setUrl2Graph] = useState('');
	const [graph1Info, setGraph1Info] = useState({});
	const [graph2Info, setGraph2Info] = useState({});
	const [dataLoaded, setDataLoaded] = useState(false);

	const handleSubmit = async e => {
		e.preventDefault();
		setDataLoaded(false);
		setLoading(true);

		try {
			const data = await getDetails(firstUrl, secondUrl);
			setUrl1Graph(`data:image/png;base64,${data.data.graph1.image}`);
			setUrl2Graph(`data:image/png;base64,${data.data.graph2.image}`);
			const { graph1, graph2 } = data.data;

			setGraph1Info({
				general: graph1.general,
				title: graph1.reasons.title,
				info: graph1.reasons.info,
			});

			setGraph2Info({
				general: graph2.general,
				title: graph2.reasons.title,
				info: graph2.reasons.info,
			});

			setDataLoaded(true);
		} catch (error) {
			console.log('error', error);
		} finally {
			setLoading(false);
		}
	};

	return (
		<Box
			sx={{
				display: 'flex',
				flexDirection: 'column',
				alignItems: 'center',
				justifyContent: 'center',
				height: '100vh',
				fontFamily: 'Comic Sans MS, Comic Sans, cursive',
				backgroundImage: `linear-gradient(to bottom right, #f1c40f, #2ecc71)`,
			}}
		>
			<Stack justifyContent='space-around'>
				{loading && <img src={Loading} alt='loading' width={800} />}
			</Stack>

			{!dataLoaded && !loading && (
				<Stack
					alignItems='center'
					justifyContent='center'
					height='100vh'
					width={800}
				>
					<InputCard
						handleSubmit={handleSubmit}
						firstUrl={firstUrl}
						setFirstUrl={setFirstUrl}
						secondUrl={secondUrl}
						setSecondUrl={setSecondUrl}
					/>
				</Stack>
			)}

			{dataLoaded && (
				<Stack justifyContent='space-around' mb='12rem'>
					<Stack direction='row' gap={5}>
						<GraphCard
							imgSrc={url1Graph}
							caption={graph1Info.general}
							title={graph1Info.title}
							bullets={graph1Info.info}
						/>
						<GraphCard
							imgSrc={url2Graph}
							caption={graph2Info.general}
							title={graph2Info.title}
							bullets={graph2Info.info}
						/>
					</Stack>
				</Stack>
			)}

			{dataLoaded && (
				<Button
					onClick={() => {
						setDataLoaded(false);
						setFirstUrl('');
						setSecondUrl('');
					}}
					variant='contained'
					sx={{
						padding: '18px 36px',
						fontSize: '1.5rem',
						backgroundColor: '#388E3C',
						color: '#fff',
						'&:hover': {
							backgroundColor: '#1B5E20',
						},
						borderRadius: '1rem',
					}}
				>
					Try Again
				</Button>
			)}
		</Box>
	);
}

export default App;
