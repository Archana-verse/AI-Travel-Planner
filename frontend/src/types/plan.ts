
export interface FormData {
  from: string;
  to: string;
  departureDate: string;
  returnDate: string;
  travelClass: string;
  budget: string;
  travelers: string;
  interests: string[];
  diet: string;
  hotelAffordability: 'low' | 'medium' | 'high';
}

