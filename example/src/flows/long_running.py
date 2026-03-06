from ststeroids import Flow, FlowContext
import time
from components import StatusComponent
from shared import ComponentIDs

class LongRunningFlow(Flow):
    @property
    def cp_spinner(self):
        return StatusComponent.get(ComponentIDs.spinner)
    
    def run(self, ctx: FlowContext):
        self.cp_spinner.set_status("Long running call", "running")
        ctx.schedule(self._long_running_method)
 
        
    def _long_running_method(self):
        time.sleep(5)
        self.cp_spinner.clear()
