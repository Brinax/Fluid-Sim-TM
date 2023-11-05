#include <stdio.h>
#include <stdlib.h>
struct Vector2* create_vector2(float, float);
void vector2__init(struct Vector2*,float, float);
void density_diffusion();
int main() {

    int gridwidth=50,gridheight=50,densities[gridwidth][gridheight],velocities[gridwidth][gridheight];
    int boundsDensity=0;
    struct Vector2 *adjacentVectors[]={create_vector2(1,0),create_vector2(-1,0),create_vector2(0,1),create_vector2(0,-1)},*boundsVelocity;
    float diffusionConst=0.01,viscosity=0.001;
    int viscosityAccuracy=20,diffusionAcuracy=20,divergenceAcuracy=20;
    int numberOfSteps=500;

    void density_diffusion()
    {
        int EqArray[5][gridwidth][gridheight];
        int varsEqArray[4][gridwidth][gridheight];
        for(int xindex;xindex<gridwidth;xindex++)
        {
            for(int yindex;yindex<gridheight;yindex++)
            {
                float varsFactors=diffusionConst/((1+diffusionConst)*4);
                EqArray[0][xindex][yindex]=varsFactors;
                EqArray[1][xindex][yindex]=varsFactors;
                EqArray[2][xindex][yindex]=varsFactors;
                EqArray[3][xindex][yindex]=varsFactors;
                EqArray[4][xindex][yindex]=densities[xindex][yindex]/(1+diffusionConst);
            }
        }
        densities[0][0]=1;
    }

    for(int index=0;index<numberOfSteps;index++)
    {
        density_diffusion();
    }
    return 0;
}

struct Vector2
{
   float x;
   float y;
};
struct Vector2* create_vector2(float x, float y)
{
    struct Vector2* result=(struct Vector2*)malloc(sizeof(struct Vector2));
    vector2__init(result,x,y);
    return result;
}
void vector2__init(struct Vector2* self,float x, float y)
{
    (*self).x=x;//or self->x=x
    (*self).y=x;
}

