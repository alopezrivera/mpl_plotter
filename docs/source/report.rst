.. You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

This title will not display
===========================
.. It is important though: without it, Sphinx will ignore everything until the 
   __second__ header it finds. This is quite inconvenient and __very__ difficult 
   to debug if you find yourself in the situation, as you will get no warning of
   what is going on.
   
   Use this to your advantage.

   You may not intend to write chapters by hand beyond the introduction. This is
   gonna yield you a 1 page chapter, and an __n__ section chapter with everything
   generated from your code.

   __Remove the non-title above__ if you want to make the __sections__ of the
   documentation generated from your code into __chapters__.

   Remember however: this will cause __everything__ in your package's __init__.py 
   to __not__ render.

.. toctree::
    :glob:
    :caption: Table of Contents
    
    intro
    chapters/*
