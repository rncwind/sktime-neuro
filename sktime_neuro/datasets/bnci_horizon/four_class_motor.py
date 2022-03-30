import pooch
import os

downloader = pooch.create(
    path=pooch.os_cache("sktime_neuro"),
    base_url="https://lampx.tugraz.at/~bci/database/001-2014/",
    registry={
        "A01T": "sha256:054f02e70cf9c4ada1517e9b9864f45407939c1062c6793516585c6f511d0325",
        "A01E": "sha256:53d415f39c3d7b0c88b894d7b08d99bcdfe855ede63831d3691af1a45607fb62",
        "A02T": "sha256:5ddd5cb520b1692c3ba1363f48d98f58f0e46f3699ee50d749947950fc39db27",
        "A02E": "sha256:d63c454005d3a9b41d8440629482e855afc823339bdd0b5721842a7ee9cc7b12",
        "A03T": "sha256:7e731ee8b681d5da6ecb11ae1d4e64b1653c7f15aad5d6b7620b25ce53141e80",
        "A03E": "sha256:d4229267ec7624fa8bd3af5cbebac17f415f7c722de6cb676748f8cb3b717d97",
        "A04T": "sha256:15850d81b95fc88cc8b9589eb9b713d49fa071e28adaf32d675b3eaa30591d6e",
        "A04E": "sha256:81916dff2c12997974ba50ffc311da006ea66e525010d010765f0047e771c86a",
        "A05T": "sha256:77387d3b669f4ed9a7c1dac4dcba4c2c40c8910bae20fb961bb7cf5a94912950",
        "A05E": "sha256:8b357470865610c28b2f1d351beac247a56a856f02b2859d650736eb2ef77808",
        "A06T": "sha256:4dc3be1b0d60279134d1220323c73c68cf73799339a7fb224087a3c560a9a7e2",
        "A06E": "sha256:bf67a40621b74b6af7a986c2f6edfff7fc2bbbca237aadd07b575893032998d1",
        "A07T": "sha256:43b6bbef0be78f0ac2b66cb2d9679091f1f5b7f0a5d4ebef73d2c7cc8e11aa96",
        "A07E": "sha256:b9aaec73dcee002fab84ee98e938039a67bf6a3cbf4fc86d5d8df198cfe4c323",
        "A08T": "sha256:7a4b3bd602d5bc307d3f4527fca2cf076659e94aca584dd64f6286fd413a82f2",
        "A08E": "sha256:0eedbd89790c7d621c8eef68065ddecf80d437bbbcf60321d9253e2305f294f7",
        "A09T": "sha256:b28d8a262c779c8cad9cc80ee6aa9c5691cfa6617c03befe490a090347ebd15c",
        "A09E": "sha256:5d79649a42df9d51215def8ffbdaf1c3f76c54b88b9bbaae721e8c6fd972cc36",
    }
)
