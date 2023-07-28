'use client';
import { Box, Button, Stack } from '@mui/material';
import Image from 'next/image';
import { useState } from 'react';
import Loading from './assets/LoadingToaster.gif';
import InputCard from './components/InputCard';
import GraphCard from './components/GraphCard';

export default function Home() {
	const [loading, setLoading] = useState(false);

	const [firstUrl, setFirstUrl] = useState('');
	const [secondUrl, setSecondUrl] = useState('');

	const [url1Graph, setUrl1Graph] = useState('');
	const [url2Graph, setUrl2Graph] = useState('');
	const [dataLoaded, setDataLoaded] = useState(false);

	// FOR DEMO
	const [graph1Info, setGraph1Info] = useState<GraphInfo>({} as GraphInfo);
	const [graph2Info, setGraph2Info] = useState({} as GraphInfo);

	const handleSubmit = async () => {
		setLoading(true);
		const res = await fetch('http://localhost:5000/api/compare', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ url1: firstUrl, url2: secondUrl }),
		});
		const data = await res.json();
		console.log(data);
		setUrl1Graph(data.url1);
		setUrl2Graph(data.url2);
		setGraph1Info(data.graph1Info);
		setGraph2Info(data.graph2Info);
		setDataLoaded(true);
		setLoading(false);
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
				{loading && <Image src={Loading} alt='loading' width={800} />}
			</Stack>

			{!dataLoaded && !loading && (
				<Stack
					alignItems='center'
					justifyContent='center'
					height='100vh'
					width='800px'
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
					onClick={() => setDataLoaded(false)}
					variant='contained'
				>
					Try Again
				</Button>
			)}
		</Box>
	);
}
