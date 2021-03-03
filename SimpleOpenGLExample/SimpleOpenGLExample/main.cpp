//Note for running this on the lab computers:
//You may need to change the windows SDK version the solution targets (right click the Solution file in the explorer, click Retarget Solution)

#include <windows.h>
#include <gl/gl.h>
#include <gl/glu.h>
#include <gl/glut.h>

//define window parameters
const int windowWidth = 300; 
const int windowHeight = 400;
//define our vertices and edges
const int numVertices = 5;  const int numEdges = 6;
const float vertices[numVertices][2] = { { 0.0, 0.0 },{ 100.0, 0.0 },
					  { 0.0, 100.0 },{ 100.0, 100.0 },{ 50.0, 150. } };	//array of 2d vertices
const int edges[numEdges][2] = { { 0, 1 },{ 1, 3 },{ 3, 2 },
								 { 2, 0 },{ 2, 4 },{ 3, 4 } };	//array of edges defined by the indices of the vertices they use

void createWindow()
{
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);  	//Set the type of window: single buffered colour window
	glutInitWindowSize(windowWidth, windowHeight); 	//Set the window width & height
	glutInitWindowPosition(300, 300);				//Set the window position on monitor
	glutCreateWindow("Simple OpenGL Example");		//Create the window
}

//set up the window and projection
void init()
{
	glClearColor(1.0, 1.0, 1.0, 0.0);	//Clearing color (for glClear) set to white. This means white background wherever we don't draw anything
	GLdouble halfWidth = (GLdouble)windowWidth / 2.0;
	GLdouble halfHeight = (GLdouble)windowHeight / 2.0;
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluOrtho2D(-halfWidth, halfWidth, -halfHeight, halfHeight);	//initialize view (simple orthographic projection)
}

//draw everything
void display()
{
	glClear(GL_COLOR_BUFFER_BIT);	//blank everything
	glColor3f(1.0f, 0.0f, 0.0f);	//Drawing in red
	glBegin(GL_LINES);
	for (int i = 0; i<numEdges; i++) 
	{
		glVertex2fv(vertices[edges[i][0]]);	//first vertex of the edge
		glVertex2fv(vertices[edges[i][1]]);	//second vertex of the edge
	}
	glEnd();
	glFlush();	//tell openGL to go ahead and draw everything we have buffered
}

//entry point to the code
int main(int argc, char** argv)	//argc and argv are for arguments given when running the program from the command line. We don't use them
{
	glutInit(&argc, argv);						//glut wants the command line parameters to init, even if they're empty
	createWindow();
	init();											//call our initialization code
	glutDisplayFunc(display);						//tell GLUT that display() is the function we use to draw
	glutMainLoop();									//enters GLUT event processing loop
}