#include <iostream>
#include <vector>
#include <string>
#include <math.h>

using namespace std;

class Vector3
{
public:
    double x;
    double y;
    double z;
    Vector3()
    {
        x = 0.0;
        y = 0.0;
        z = 0.0;
    }
    Vector3(double xVal, double yVal, double zVal)
    {
        x = xVal;
        y = yVal;
        z = zVal;
    }
};

double dot(Vector3 u, Vector3 v)
{
    return u.x * v.x + u.y * v.y + u.z * v.z;
}

Vector3 cross(Vector3 u, Vector3 v)
{
    double crossX = (u.y * v.z - u.z * v.y);
    double crossY = (u.z * v.x - u.x * v.z);
    double crossZ = (u.x * v.y - u.y * v.x);

    return Vector3(crossX, crossY, crossZ);
}

Vector3 lerp(Vector3 u, Vector3 v, double t)
{
    // Vector3 crossVec = cross(u, v);
    double learpX = u.x + (v.x - u.x) * t;
    double learpY = u.y + (v.y - u.y) * t;
    double learpZ = u.z + (v.z - u.z) * t;

    // return Vector3(crossVec.x * t, crossVec.y * t, crossVec.z * t);
    return Vector3(learpX, learpY, learpZ);
}

double magnitude(Vector3 u)
{
    return sqrt((pow(u.x, 2)) + (pow(u.y, 2)) + (pow(u.z, 2)));
}

Vector3 transformCoordinateSystem(Vector3 point, Vector3 u, Vector3 v, Vector3 n, Vector3 uvnOrigin, Vector3 a, Vector3 b, Vector3 c, Vector3 abcOrigin)
{

    // transpose
    Vector3 u1 = Vector3(u.x, v.x, n.x);
    Vector3 v1 = Vector3(u.y, v.y, n.y);
    Vector3 n1 = Vector3(u.z, v.z, n.z);

    Vector3 r1 = Vector3(dot(point, u1), dot(point, v1), dot(point, n1));

    // p world
    Vector3 pw = Vector3((r1.x + uvnOrigin.x), (r1.y + uvnOrigin.y), (r1.z + uvnOrigin.z));

    Vector3 r2 = Vector3((pw.x - abcOrigin.x), (pw.y - abcOrigin.y), (pw.z - abcOrigin.z));

    Vector3 p1 = Vector3(dot(a, r2), dot(b, r2), dot(c, r2));

    return p1;
}

int main()
{
    // q1
    // Vector3 u = {3.0, -1.0, 2.0};
    // Vector3 v = {2.0, 1.0, 2.0};
    // double f = dot(u, v);
    // printf("u.v = %.2lf", f);

    // q2
    // Vector3 a = Vector3(3.0, -1.0, 2.0);
    // Vector3 b = Vector3(2.0, 1.0, 2.0);
    // Vector3 result = lerp(a, b, 0.5);
    // printf("(%.2lf, %.2lf, %.2lf)", result.x, result.y, result.z);

    // q3

    Vector3 p = Vector3(0.0, 2.0, 0.0);
    Vector3 u = Vector3(0.0, 1.0, 0.0);
    Vector3 v = Vector3(-1.0, 0.0, 0.0);
    Vector3 n = Vector3(0.0, 0.0, 1.0);
    Vector3 uvnOrigin = Vector3(0.0, 2.0, 4.0);
    Vector3 a = Vector3(1.0, 0.0, 0.0);
    Vector3 b = Vector3(0.0, 1.0, 0.0);
    Vector3 c = Vector3(0.0, 0.0, 1.0);
    Vector3 abcOrigin = Vector3(0.0, 0.0, 0.0);
    Vector3 tp = transformCoordinateSystem(p, u, v, n, uvnOrigin, a, b, c, abcOrigin);
    printf("(%.2lf, %.2lf, %.2lf)", tp.x, tp.y, tp.z);
}