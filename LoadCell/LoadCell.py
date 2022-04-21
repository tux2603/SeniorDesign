# All weights are in grams

from threading import Thread

class LoadCell:
    def __init__(self):
        # need to connect to pi
        
        self.offset = 0.0 # need to calculate each time? - incase of leftover liquid?
        self.endWeight = 0.0
        self.capacityWeight = 780.0
        
        # Var to stop thread
        self._terminate = False
        
    @property
    def offset(self):
        return self.offset
    
    @property
    def endWeight(self):
        return self.endweight
    
    @property
    def capacityWeight(self):
        return self.capacityweight
    
    def calculateOffset(self):
        #self.offset = 975 * Measured Output (with nothing on load cell)
        pass
    
    def calculateEndWeight(self):
        # endWeight = 975 * Measured Output(mV/V) + Offset
        # 975 comes from: Capacity / Rated Output = 780 / 0.8
        pass
    
    def start(self):
        self._thread = Thread(target=self._processing_thread)
        self._thread.start()
    
    def stop(self):
        self._terminate = True
        self._thread.join()
        
    def _processing_thread(self):
        self.calculateOffset()
        while not self._terminate:
            # print('LoadCell: Processing thread running')
            self.calculateEndWeight()
            if self.endWeight > self.capacityWeight:
                print("TOO HEAVY")
                break