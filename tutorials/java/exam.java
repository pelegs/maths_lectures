public int f(int x[], int a)
{
    int i = 0;
    boolean b = true;
    while (b && (i < x.length))
    {
        if (x[i] == a)
            b = false
        else
            i = i+1;
    }
    if (b)
    {
        println("Error!");
        return -1;
    }
    else
        return i;
}
