import React from 'react';
import { Stack, Typography } from '@mui/material';

const GraphCard = ({ imgSrc, caption, title, bullets }) => {
	return (
		<Stack>
			<Stack
				mx="auto"
				sx={{
					borderRadius: '1rem',
					boxShadow: '0 0 10px rgba(0, 0, 0, 0.3)',
					backgroundColor: 'white',
					alignItems: 'center',
				}}
			>
				<img
					src={imgSrc || ''}
					alt="Graph1"
					width={800}
					style={{
						borderRadius: '1rem',
					}}
				/>
				<Typography
					variant="h6"
					textAlign="center"
					mx="5rem"
					mt="1rem"
					width={800}
					p={2}
				>
					{caption}
				</Typography>
			</Stack>

			<Stack
				mt={4}
				ml="auto"
				mr="auto"
				sx={{
					borderRadius: '1rem',
					boxShadow: '0 0 10px rgba(0, 0, 0, 0.3)',
					backgroundColor: 'white',
					width: 800,
					padding: '2rem',
				}}
			>
				<Typography variant="h6">{title}</Typography>

				{bullets?.map((item, index) => (
					<Typography
						component="li"
						key={index}
						variant="body1"
						sx={{
							marginLeft: '1rem',
							color: '#444',
						}}
					>
						{item}
					</Typography>
				))}
			</Stack>
		</Stack>
	);
};

export default GraphCard;
