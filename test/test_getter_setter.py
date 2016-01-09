from fileperms import Permission, Permissions


class TestGetterSetter:
    def test_empty(self):
        prm = Permissions()
        for item in Permission:
            assert prm.get(item) == False

    def test_other(self):
        prm = Permissions()
        for item in Permission:
            prm.set(item, True)
            assert prm.get(item) == True

            prm.set(item, False)
            assert prm.get(item) == False
