interface Event {
	id: number;
	attributes: {
		title: string;
		description: string;
		startDate: string;
		endDate: string;
		startTime: string;
		endTime?: string;
	};
}

//singular form of News
interface New {
	id: number;
	attributes: {
		title: string;
		description: string;
		updatedAt: string;
	};
}

interface Carousel {
	id: number;
	attributes: {
		description: string;
		image: {
			data: {
				attributes: {
					url: string
				}
			}
		};
	}
}

export type { Event, New, Carousel };
