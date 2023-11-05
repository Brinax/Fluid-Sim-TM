if __name__ == "__main__":
        
    import os
    os.environ["PYSDL2_DLL_PATH"] = "C:\\Users\\lcach\\Downloads\\SDL2-2.28.3-win32-x64"
    import hienoi.application
    from hienoi import Vector2f
    def initialize_particle_simulation(sim):
        sim.add_particle(position=Vector2f(25.0, 0.0))
    def update_particle_simulation(sim):
        particle = sim.particles[0]
        particle.force -= particle.position
    hienoi.application.run(
        particle_simulation={
            'initialize_callback': initialize_particle_simulation,
            'postsolve_callback': update_particle_simulation,
        })