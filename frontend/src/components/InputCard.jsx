import React from 'react';
import { Box, Typography, TextField, Button, Stack } from '@mui/material';

const InputCard = ({
	firstUrl,
	setFirstUrl,
	secondUrl,
	setSecondUrl,
	handleSubmit,
}) => {
	const handleFirstUrlChange = (e) => {
		setFirstUrl(e.target.value);
	};

	const handleSecondUrlChange = (e) => {
		setSecondUrl(e.target.value);
	};

	return (
		<Stack
			sx={{
				background: '#fff',
				padding: '5rem',
				borderRadius: '1rem',
				boxShadow: '0 0 10px rgba(0, 0, 0, 0.3)',
			}}
			textAlign="center"
			alignItems="center"
		>
			<Typography
				variant="h2"
				sx={{
					marginBottom: '1rem',
					color: '#2ecc71',
					fontWeight: 'bold',
					textShadow: '2px 2px #f1c40f',
				}}
			>
				Compare Yelp Ratings
			</Typography>

			<Typography variant="h5" sx={{ marginBottom: '1rem', color: '#444' }}>
				Please Enter Two Yelp URLs
			</Typography>

			<Stack direction="row">
				<Box
					component="form"
					onSubmit={handleSubmit}
					sx={{ display: 'flex', alignItems: 'center' }}
				>
					<TextField
						type="text"
						label="Enter URL 1"
						variant="outlined"
						onChange={handleFirstUrlChange}
						sx={{
							marginRight: '0.5rem',
							'& fieldset': { borderColor: '#2ecc71' },
						}}
						value={firstUrl}
					/>

					<TextField
						type="text"
						label="Enter URL 2"
						variant="outlined"
						onChange={handleSecondUrlChange}
						sx={{
							marginRight: '0.5rem',
							'& fieldset': { borderColor: '#2ecc71' },
						}}
						value={secondUrl}
					/>

					<Button
						type="submit"
						variant="contained"
						sx={{
							backgroundColor: '#2ecc71',
							color: '#fff',
							height: 'fit-content',
							fontSize: '1.2rem',
							py: 1,
							'&:hover': {
								backgroundColor: '#27ae60',
								boxShadow: '0 0 10px rgba(0, 0, 0, 0.5)',
							},
						}}
					>
						Submit
					</Button>
				</Box>
			</Stack>
		</Stack>
	);
};

export default InputCard;
