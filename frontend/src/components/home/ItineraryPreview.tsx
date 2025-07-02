
import React from 'react';
import { MapPin, Clock, Camera, Utensils, Brain } from 'lucide-react';

const ItineraryPreview = () => {
  return (
    <div className="py-20 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-heading mb-4">Planning a trip to Goa? 🏖️</h2>
          <p className="text-body max-w-2xl mx-auto">
            See how Raahi creates intelligent, personalized itineraries that maximize your experience while respecting your time and budget.
          </p>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-6">
            <div className="card-elevated p-6">
              <div className="flex items-center mb-4">
                <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center mr-4">
                  <Clock className="text-primary" size={20} />
                </div>
                <div>
                  <h3 className="font-semibold text-foreground">Day 1 - Arrival & North Goa</h3>
                  <p className="text-sm text-muted-foreground">9:00 AM - 8:00 PM</p>
                </div>
              </div>
              <div className="space-y-3 ml-14">
                <div className="flex items-center text-sm">
                  <MapPin className="text-primary mr-2" size={16} />
                  <span>Land at Goa Airport → Check into beachside resort</span>
                </div>
                <div className="flex items-center text-sm">
                  <Camera className="text-primary mr-2" size={16} />
                  <span>Explore Baga Beach & water sports</span>
                </div>
                <div className="flex items-center text-sm">
                  <Utensils className="text-primary mr-2" size={16} />
                  <span>Sunset dinner at Tito's Lane</span>
                </div>
              </div>
            </div>
            
            <div className="card-elevated p-6">
              <div className="flex items-center mb-4">
                <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center mr-4">
                  <Clock className="text-primary" size={20} />
                </div>
                <div>
                  <h3 className="font-semibold text-foreground">Day 2 - Cultural Immersion</h3>
                  <p className="text-sm text-muted-foreground">8:00 AM - 7:00 PM</p>
                </div>
              </div>
              <div className="space-y-3 ml-14">
                <div className="flex items-center text-sm">
                  <MapPin className="text-primary mr-2" size={16} />
                  <span>Visit Basilica of Bom Jesus & Se Cathedral</span>
                </div>
                <div className="flex items-center text-sm">
                  <Camera className="text-primary mr-2" size={16} />
                  <span>Spice plantation tour with traditional lunch</span>
                </div>
                <div className="flex items-center text-sm">
                  <Utensils className="text-primary mr-2" size={16} />
                  <span>Evening at Anjuna Flea Market</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="relative">
            <div className="card-elevated p-8 bg-gradient-to-br from-primary/5 to-green-500/5">
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-br from-primary to-green-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <Brain className="text-white" size={28} />
                </div>
                <h3 className="text-xl font-semibold mb-4">AI-Powered Intelligence</h3>
                <div className="space-y-4 text-left">
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-sm text-muted-foreground">Real-time weather and crowd data integration</p>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-sm text-muted-foreground">Budget optimization with smart recommendations</p>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-sm text-muted-foreground">Cultural preferences and dietary restrictions considered</p>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-sm text-muted-foreground">Live booking integration with best prices</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ItineraryPreview;
